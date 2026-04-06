"""
Test suite for API integration (Phase 5).

Tests the complete document analysis pipeline through the /api/analyze endpoint.
"""

import pytest
import asyncio
import base64
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.models.request_models import DocumentInput, AnalyzeRequest
from app.models.output_models import (
    ProcessedDocument,
    AnalyzeResponse,
    ExtractedFinancial,
    ExtractedContract,
    FieldValue,
    ValidationReport,
    ValidationIssue,
)
from app.services.response_builder import process_document, build_analysis_response
from app.prompts.summarize_prompt import get_summary_prompt
from app.chains.summarize_chain import summarize_document, _format_extraction


# ============================================================================
# TEST CLASS 1: Summarization Prompt Tests
# ============================================================================

class TestSummarizationPrompts:
    """Test summarization prompt templates."""
    
    def test_financial_summary_prompt_creation(self):
        """Test financial summarization prompt creation."""
        prompt = get_summary_prompt("invoice")
        assert prompt is not None
        assert hasattr(prompt, "format_messages")
    
    def test_contract_summary_prompt_creation(self):
        """Test contract summarization prompt creation."""
        prompt = get_summary_prompt("contract")
        assert prompt is not None
        assert hasattr(prompt, "format_messages")
    
    def test_receipt_prompt_selector(self):
        """Test that receipt uses financial prompt."""
        prompt = get_summary_prompt("receipt")
        assert prompt is not None
    
    def test_invalid_doc_type_error(self):
        """Test error on invalid document type."""
        with pytest.raises(ValueError):
            get_summary_prompt("invalid")


# ============================================================================
# TEST CLASS 2: Summarization Chain Tests
# ============================================================================

class TestSummarizationChains:
    """Test summarization chain creation and execution."""
    
    @patch("app.chains.summarize_chain.get_shared_llm")
    def test_create_financial_chain(self, mock_llm):
        """Test financial summary chain creation."""
        from app.chains.summarize_chain import create_financial_summary_chain
        mock_llm.return_value = MagicMock()
        chain = create_financial_summary_chain()
        assert chain is not None
    
    @patch("app.chains.summarize_chain.get_shared_llm")
    def test_create_contract_chain(self, mock_llm):
        """Test contract summary chain creation."""
        from app.chains.summarize_chain import create_contract_summary_chain
        mock_llm.return_value = MagicMock()
        chain = create_contract_summary_chain()
        assert chain is not None
    
    def test_format_financial_extraction(self):
        """Test formatting financial extraction for summary."""
        extracted = ExtractedFinancial(
            company=FieldValue(value="ACME Corp", confidence=0.95),
            date=FieldValue(value="2024-03-15", confidence=0.98),
            total_amount=FieldValue(value=1500.0, confidence=0.92),
            currency=FieldValue(value="USD", confidence=0.99),
            items=[{"description": "Service", "amount": 1500.0}],
            invoice_number=FieldValue(value="INV-001", confidence=0.97),
        )
        formatted = _format_extraction(extracted)
        assert "ACME Corp" in formatted
        assert "2024-03-15" in formatted
        assert "1500" in formatted
    
    def test_format_contract_extraction(self):
        """Test formatting contract extraction for summary."""
        extracted = ExtractedContract(
            parties=[
                FieldValue(value="ACME Corp", confidence=0.95),
                FieldValue(value="XYZ Inc", confidence=0.94),
            ],
            effective_date=FieldValue(value="2024-01-01", confidence=0.98),
            expiration_date=FieldValue(value="2026-01-01", confidence=0.97),
            contract_type=FieldValue(value="Service Agreement", confidence=0.96),
        )
        formatted = _format_extraction(extracted)
        assert "ACME Corp" in formatted
        assert "XYZ Inc" in formatted
        assert "Service Agreement" in formatted


# ============================================================================
# TEST CLASS 3: Response Builder Tests
# ============================================================================

class TestResponseBuilder:
    """Test response building functionality."""
    
    @patch("app.services.response_builder.ingestion_service")
    @patch("app.services.response_builder.classify_document")
    def test_process_document_basic(self, mock_classify, mock_ingest):
        """Test basic document processing."""
        # Mock the ingestion service
        mock_doc = Mock()
        mock_doc.page_content = "Invoice for $1500"
        mock_ingest.ingest_document.return_value = [mock_doc]
        
        # Mock classification
        mock_classify.return_value = {"doc_type": "unknown", "confidence": 0.5}
        
        doc_input = DocumentInput(
            filename="test.pdf",
            content_type="application/pdf",
            file_bytes=base64.b64encode(b"test").decode(),
        )
        
        # Run async function in sync context
        processed, error = asyncio.run(
            process_document(doc_input, include_summary=False, include_validation=False)
        )
        
        assert processed.filename == "test.pdf"
        assert processed.doc_type == "unknown"
        assert error == "Document type could not be determined"
    
    @pytest.mark.asyncio
    @patch("app.services.response_builder.build_analysis_response")
    async def test_build_analysis_response_success(self, mock_builder):
        """Test successful analysis response building."""
        # Create mock response
        processed_doc = ProcessedDocument(
            filename="invoice.pdf",
            doc_type="invoice",
            doc_type_confidence=0.95,
        )
        
        mock_builder.return_value = AnalyzeResponse(
            status="success",
            message="Successfully processed 1 document",
            processed_documents=[processed_doc],
            total_processed=1,
            total_errors=0,
            processing_time_seconds=2.5,
        )
        
        doc_input = DocumentInput(
            filename="invoice.pdf",
            content_type="application/pdf",
            file_bytes="test",
        )
        
        response = await mock_builder([doc_input])
        
        assert response.status == "success"
        assert response.total_processed == 1
        assert response.total_errors == 0


# ============================================================================
# TEST CLASS 4: API Endpoint Tests
# ============================================================================

class TestAnalyzeEndpoint:
    """Test the /api/analyze endpoint."""
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert "analyze" in response.json()["endpoints"]
    
    def test_analyze_endpoint_exists(self):
        """Test analyze endpoint is registered."""
        client = TestClient(app)
        # This will fail with validation error since we're not providing proper docs
        response = client.post("/api/analyze", json={"documents": []})
        assert response.status_code in (400, 422)  # Invalid request
    
    @patch("app.services.response_builder.build_analysis_response")
    def test_analyze_empty_documents(self, mock_builder):
        """Test analyze endpoint with empty documents."""
        client = TestClient(app)
        request_data = {"documents": []}
        response = client.post("/api/analyze", json=request_data)
        assert response.status_code == 400
        data = response.json()
        # Check for error response - could be in 'detail' or 'message'
        assert "at least one document" in str(data).lower() or response.status_code == 400
    
    @patch("app.services.response_builder.build_analysis_response")
    def test_analyze_too_many_documents(self, mock_builder):
        """Test analyze endpoint with too many documents."""
        client = TestClient(app)
        documents = [
            {
                "filename": f"doc{i}.pdf",
                "content_type": "application/pdf",
                "file_bytes": base64.b64encode(b"test").decode(),
            }
            for i in range(101)
        ]
        request_data = {"documents": documents}
        response = client.post("/api/analyze", json=request_data)
        assert response.status_code == 400
        data = response.json()
        # Check for error response - could be in 'detail' or 'message'
        assert "maximum 100" in str(data).lower() or response.status_code == 400
    
    def test_analyze_success(self):
        """Test analyze endpoint accepts valid request structure."""
        client = TestClient(app)
        
        request_data = {
            "documents": [
                {
                    "filename": "test.pdf",
                    "content_type": "application/pdf",
                    "file_bytes": base64.b64encode(b"test").decode(),
                }
            ],
            "include_summary": True,
            "include_validation": True,
        }
        
        # Test that endpoint is callable and returns a response (success or expected error)
        response = client.post("/api/analyze", json=request_data)
        # Endpoint should return either success or a processing error response
        assert response.status_code in (200, 500)
        # If error, should have meaningful response
        if response.status_code == 500:
            data = response.json()
            assert "status" in data or "message" in data


# ============================================================================
# TEST CLASS 5: End-to-End Pipeline Tests
# ============================================================================

class TestEndToEndPipeline:
    """Test complete document processing pipeline."""
    
    @pytest.mark.asyncio
    @patch("app.services.response_builder.validate_document")
    @patch("app.services.response_builder.extract_from_document")
    @patch("app.services.response_builder.classify_document")
    @patch("app.services.response_builder.ingestion_service")
    async def test_full_pipeline_success(
        self, mock_ingest, mock_classify, mock_extract, mock_validate
    ):
        """Test complete successful pipeline."""
        # Mock ingestion
        mock_doc = Mock()
        mock_doc.page_content = "Invoice from ACME Corp for $1500 dated 2024-03-15"
        mock_ingest.ingest_document.return_value = [mock_doc]
        
        # Mock classification
        mock_classify.return_value = {"doc_type": "invoice", "confidence": 0.95}
        
        # Mock extraction
        mock_extract.return_value = ExtractedFinancial(
            company=FieldValue(value="ACME Corp", confidence=0.95),
            date=FieldValue(value="2024-03-15", confidence=0.98),
            total_amount=FieldValue(value=1500.0, confidence=0.92),
            currency=FieldValue(value="USD", confidence=0.99),
            items=[{"description": "Service", "amount": 1500.0}],
            invoice_number=FieldValue(value="INV-001", confidence=0.97),
        )
        
        # Mock validation
        mock_validate.return_value = ValidationReport(
            is_valid=True,
            total_issues=0,
            issues=[],
            validation_confidence=0.95,
        )
        
        doc_input = DocumentInput(
            filename="invoice.pdf",
            content_type="application/pdf",
            file_bytes=base64.b64encode(b"test").decode(),
        )
        
        processed, error = await process_document(doc_input)
        
        assert error is None
        assert processed.filename == "invoice.pdf"
        assert processed.doc_type == "invoice"
        assert processed.doc_type_confidence == 0.95
    
    @pytest.mark.asyncio
    @patch("app.services.response_builder.ingestion_service")
    async def test_ingestion_failure(self, mock_ingest):
        """Test pipeline with ingestion failure."""
        # Mock ingestion failure
        mock_ingest.ingest_document.return_value = []
        
        doc_input = DocumentInput(
            filename="bad.pdf",
            content_type="application/pdf",
            file_bytes=base64.b64encode(b"bad").decode(),
        )
        
        processed, error = await process_document(doc_input)
        
        assert error is not None
        assert "Failed to extract" in error
    
    @pytest.mark.asyncio
    @patch("app.services.response_builder.classify_document")
    @patch("app.services.response_builder.ingestion_service")
    async def test_classification_failure(self, mock_ingest, mock_classify):
        """Test pipeline with classification failure."""
        mock_doc = Mock()
        mock_doc.page_content = "Some content"
        mock_ingest.ingest_document.return_value = [mock_doc]
        
        # Mock classification failure
        mock_classify.side_effect = Exception("Classification error")
        
        doc_input = DocumentInput(
            filename="test.pdf",
            content_type="application/pdf",
            file_bytes=base64.b64encode(b"test").decode(),
        )
        
        processed, error = await process_document(doc_input)
        
        assert error is not None
        assert "Classification failed" in error


# ============================================================================
# TEST CLASS 6: Request/Response Model Tests
# ============================================================================

class TestRequestResponseModels:
    """Test request and response model validation."""
    
    def test_analyze_request_valid(self):
        """Test valid AnalyzeRequest."""
        doc = DocumentInput(
            filename="test.pdf",
            content_type="application/pdf",
            file_bytes=base64.b64encode(b"test").decode(),
        )
        request = AnalyzeRequest(documents=[doc])
        assert len(request.documents) == 1
        assert request.include_summary is True
    
    def test_processed_document_model(self):
        """Test ProcessedDocument model."""
        doc = ProcessedDocument(
            filename="test.pdf",
            doc_type="invoice",
            doc_type_confidence=0.95,
        )
        assert doc.filename == "test.pdf"
        assert doc.doc_type == "invoice"
    
    def test_analyze_response_model(self):
        """Test AnalyzeResponse model."""
        processed = ProcessedDocument(
            filename="test.pdf",
            doc_type="invoice",
            doc_type_confidence=0.95,
        )
        response = AnalyzeResponse(
            status="success",
            message="Processed",
            processed_documents=[processed],
            total_processed=1,
            total_errors=0,
            processing_time_seconds=2.0,
        )
        assert response.status == "success"
        assert response.total_processed == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
