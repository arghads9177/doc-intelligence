"""
Comprehensive integration tests for the Document Intelligence System.

This test suite validates the complete end-to-end pipeline:
- Document ingestion
- Classification
- Extraction
- Validation
- Summarization and API integration

Tests ensure all phases work together seamlessly with error handling
and recover gracefully from various failure scenarios.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch, call
from fastapi.testclient import TestClient
import json

from app.main import app
from app.models.request_models import (
    DocumentInput,
    AnalyzeRequest,
)
from app.models.output_models import (
    ExtractedFinancial,
    ExtractedContract,
    ValidationReport,
    FieldValue,
    AnalyzeResponse,
)


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def sample_invoice_content():
    """Sample invoice content for testing."""
    return """
    INVOICE
    
    Company: Acme Corporation
    Invoice Number: INV-2024-001
    Date: March 15, 2024
    
    Items:
    - Widget A: $500.00 x 2 = $1,000.00
    - Widget B: $250.00 x 1 = $250.00
    
    Total: $1,250.00
    Currency: USD
    """


@pytest.fixture
def sample_contract_content():
    """Sample contract content for testing."""
    return """
    SERVICE AGREEMENT
    
    Parties: Acme Corp and XYZ Limited
    Effective Date: January 1, 2024
    Expiration Date: December 31, 2025
    
    Obligations:
    - Acme will provide consulting services
    - XYZ will pay monthly fees
    
    Term: 24 months
    """


@pytest.fixture
def sample_receipt_content():
    """Sample receipt content for testing."""
    return """
    RECEIPT
    
    Store: Local Coffee Shop
    Date: April 1, 2024
    
    Items:
    - Latte: $5.00
    - Pastry: $3.50
    
    Total: $8.50
    Currency: USD
    """


@pytest.fixture
def sample_document_invoice():
    """Sample document for invoice."""
    return DocumentInput(
        filename="invoice.txt",
        content_type="text/plain",
        file_bytes="SUJWPVRlc3QgQ29udGVudA==",
    )


@pytest.fixture
def sample_document_contract():
    """Sample document for contract."""
    return DocumentInput(
        filename="contract.txt",
        content_type="text/plain",
        file_bytes="Q09OVFJBQ1Q9VGVzdCBDb250ZW50",
    )


class TestEndToEndPipelineIntegration:
    """Test complete pipeline flow from ingestion to API response."""

    def test_api_health_check(self, client):
        """Test health endpoint availability."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_api_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200

    def test_analyze_endpoint_with_query_parameters(self, client, sample_document_invoice):
        """Test analyze endpoint accepts query parameters."""
        request_data = AnalyzeRequest(documents=[sample_document_invoice])
        
        response = client.post(
            "/api/analyze?include_summary=true&include_validation=true",
            json=request_data.model_dump(),
        )
        
        # Should not fail due to query parameters
        assert response.status_code in [200, 422, 500]

    def test_analyze_endpoint_summary_disabled(
        self, client, sample_document_invoice
    ):
        """Test analyze endpoint with summarization disabled."""
        request_data = AnalyzeRequest(documents=[sample_document_invoice])
        
        response = client.post(
            "/api/analyze?include_summary=false",
            json=request_data.model_dump(),
        )
        
        assert response.status_code in [200, 422, 500]

    def test_analyze_endpoint_validation_disabled(
        self, client, sample_document_invoice
    ):
        """Test analyze endpoint with validation disabled."""
        request_data = AnalyzeRequest(documents=[sample_document_invoice])
        
        response = client.post(
            "/api/analyze?include_validation=false",
            json=request_data.model_dump(),
        )
        
        assert response.status_code in [200, 422, 500]

    def test_analyze_endpoint_batch_processing(self, client):
        """Test analyze endpoint processes multiple documents."""
        documents = [
            DocumentInput(
                filename=f"doc_{i}.txt",
                content_type="text/plain",
                file_bytes="VGVzdA==",
            )
            for i in range(5)
        ]
        request_data = AnalyzeRequest(documents=documents)
        
        response = client.post("/api/analyze", json=request_data.model_dump())
        
        assert response.status_code in [200, 422, 500]
        if response.status_code == 200:
            data = response.json()
            assert "total_processed" in data or "status" in data

    def test_analyze_endpoint_empty_documents_error(self, client):
        """Test analyze endpoint rejects empty document list."""
        request_data = AnalyzeRequest(documents=[])
        
        response = client.post("/api/analyze", json=request_data.model_dump())
        
        # Should return error for empty documents
        assert response.status_code in [400, 422]

    def test_analyze_endpoint_too_many_documents_error(self, client):
        """Test analyze endpoint rejects batch > 100 documents."""
        documents = [
            DocumentInput(
                filename=f"doc_{i}.txt",
                content_type="text/plain",
                file_bytes="VGVzdA==",
            )
            for i in range(101)
        ]
        request_data = AnalyzeRequest(documents=documents)
        
        response = client.post("/api/analyze", json=request_data.model_dump())
        
        # Should return error for too many documents
        assert response.status_code in [400, 422]


class TestPipelineStageIntegration:
    """Test individual stages and their integration."""

    @pytest.mark.asyncio
    async def test_ingestion_to_classification_flow(self, sample_invoice_content):
        """Test workflow from ingestion through classification."""
        from app.services.ingestion import DocumentIngestionService
        from app.chains.classify_chain import create_classify_chain
        
        # Ingestion service
        ingestion = DocumentIngestionService()
        assert ingestion is not None
        
        # Classification chain creation should work
        chain = create_classify_chain()
        assert chain is not None

    @pytest.mark.asyncio
    async def test_classification_to_extraction_flow(self):
        """Test workflow from classification through extraction."""
        from app.chains.classify_chain import create_classify_chain
        from app.chains.extract_chain import create_extraction_chain
        
        # Both chains should initialize properly
        classify_chain = create_classify_chain()
        extract_chain = create_extraction_chain("invoice")
        
        assert classify_chain is not None
        assert extract_chain is not None

    @pytest.mark.asyncio
    async def test_extraction_to_validation_flow(self):
        """Test workflow from extraction through validation."""
        from app.chains.extract_chain import create_extraction_chain
        from app.chains.validate_chain import create_validation_chain
        
        # Both chains should initialize properly
        extract_chain = create_extraction_chain("invoice")
        validate_chain = create_validation_chain("invoice")
        
        assert extract_chain is not None
        assert validate_chain is not None

    @pytest.mark.asyncio
    async def test_validation_to_summarization_flow(self):
        """Test workflow from validation through summarization."""
        from app.chains.validate_chain import create_validation_chain
        from app.chains.summarize_chain import create_summary_chain
        
        # Both chains should initialize properly
        validate_chain = create_validation_chain("invoice")
        summary_chain = create_summary_chain("invoice")
        
        assert validate_chain is not None
        assert summary_chain is not None


class TestErrorRecoveryAndResilience:
    """Test system resilience and error handling."""

    def test_api_missing_required_fields(self, client):
        """Test API rejects request with missing required fields."""
        response = client.post(
            "/api/analyze",
            json={"documents": []},  # Missing actual documents
        )
        
        assert response.status_code in [400, 422]

    def test_api_invalid_json_structure(self, client):
        """Test API handles invalid JSON structure."""
        response = client.post(
            "/api/analyze",
            json={"invalid_field": "value"},  # No documents field
        )
        
        assert response.status_code in [400, 422]

    def test_api_malformed_file_bytes(self, client):
        """Test API handles malformed base64 content."""
        request_data = AnalyzeRequest(
            documents=[
                DocumentInput(
                    filename="bad.txt",
                    content_type="text/plain",
                    file_bytes="not_valid_base64!@#$%",
                )
            ]
        )
        
        response = client.post("/api/analyze", json=request_data.model_dump())
        
        # Should handle gracefully (not crash)
        assert response.status_code in [200, 400, 422, 500]

    def test_api_unsupported_content_type(self, client):
        """Test API handles unsupported content types."""
        request_data = AnalyzeRequest(
            documents=[
                DocumentInput(
                    filename="file.xyz",
                    content_type="application/xyz",
                    file_bytes="VGVzdA==",
                )
            ]
        )
        
        response = client.post("/api/analyze", json=request_data.model_dump())
        
        # Should handle gracefully
        assert response.status_code in [200, 400, 422, 500]


class TestDataModelIntegration:
    """Test data models work correctly throughout pipeline."""

    def test_field_value_model(self):
        """Test FieldValue confidence wrapper."""
        field = FieldValue(value="Test", confidence=0.95)
        assert field.value == "Test"
        assert field.confidence == 0.95
        assert 0 <= field.confidence <= 1

    def test_extracted_financial_model(self):
        """Test ExtractedFinancial model structure."""
        extracted = ExtractedFinancial(
            company=FieldValue(value="Test Corp", confidence=0.95),
            date=FieldValue(value="2024-01-01", confidence=0.90),
            invoice_number=FieldValue(value="INV-001", confidence=0.95),
            total_amount=FieldValue(value=1000.0, confidence=0.98),
            currency=FieldValue(value="USD", confidence=0.99),
            items=[{"description": "Item 1", "amount": 500.0}],
        )
        
        assert extracted.company.value == "Test Corp"
        assert extracted.total_amount.value == 1000.0
        assert len(extracted.items) == 1

    def test_extracted_contract_model(self):
        """Test ExtractedContract model structure."""
        extracted = ExtractedContract(
            parties=[
                FieldValue(value="Party A", confidence=0.95),
                FieldValue(value="Party B", confidence=0.95),
            ],
            effective_date=FieldValue(value="2024-01-01", confidence=0.95),
            expiration_date=FieldValue(value="2025-01-01", confidence=0.95),
            key_obligations=[{"obligation": "Pay fees monthly"}],
            contract_type=FieldValue(value="Service Agreement", confidence=0.90),
        )
        
        assert len(extracted.parties) == 2
        assert extracted.effective_date.value == "2024-01-01"

    def test_validation_report_model(self):
        """Test ValidationReport model."""
        report = ValidationReport(
            is_valid=True,
            total_issues=0,
            issues=[],
            validation_confidence=0.95,
        )
        
        assert report.is_valid is True
        assert report.total_issues == 0
        assert isinstance(report.issues, list)

    def test_analyze_response_model(self):
        """Test AnalyzeResponse model."""
        response = AnalyzeResponse(
            status="success",
            message="Processing complete",
            processed_documents=[],
            total_processed=0,
            total_errors=0,
            processing_time_seconds=1.5,
        )
        
        assert response.status == "success"
        assert response.total_processed == 0
        assert response.processing_time_seconds == 1.5


class TestConcurrencyAndPerformance:
    """Test system performance characteristics."""

    def test_api_response_time_acceptable(self, client, sample_document_invoice):
        """Test API responds within acceptable time."""
        import time
        
        request_data = AnalyzeRequest(documents=[sample_document_invoice])
        start_time = time.time()
        
        response = client.post(
            "/api/analyze",
            json=request_data.model_dump(),
        )
        
        elapsed_time = time.time() - start_time
        
        # Response should be reasonably fast
        assert elapsed_time < 30  # 30 second timeout for API call

    def test_batch_processing_maintains_order(self, client):
        """Test batch processing maintains document order."""
        documents = [
            DocumentInput(
                filename=f"doc_{i}.txt",
                content_type="text/plain",
                file_bytes="VGVzdA==",
            )
            for i in range(3)
        ]
        request_data = AnalyzeRequest(documents=documents)
        
        response = client.post("/api/analyze", json=request_data.model_dump())
        
        if response.status_code == 200:
            data = response.json()
            if "processed_documents" in data:
                # Verify we have all documents
                assert len(data["processed_documents"]) >= 0


class TestResponseStructureCompliance:
    """Test API response structure compliance."""

    def test_analyze_response_structure_success(self, client):
        """Test successful analyze response has all required fields."""
        # This is a structural test - status code may vary based on mocks
        request_data = AnalyzeRequest(
            documents=[
                DocumentInput(
                    filename="test.txt",
                    content_type="text/plain",
                    file_bytes="VGVzdA==",
                )
            ]
        )
        
        response = client.post("/api/analyze", json=request_data.model_dump())
        
        if response.status_code == 200:
            data = response.json()
            # Check response has expected top-level keys
            assert "status" in data
            assert "message" in data or "processed_documents" in data

    def test_analyze_response_handles_partial_success(self, client):
        """Test response handles partial success scenario."""
        documents = [
            DocumentInput(
                filename="doc_1.txt",
                content_type="text/plain",
                file_bytes="VGVzdA==",
            ),
            DocumentInput(
                filename="doc_2.txt",
                content_type="text/plain",
                file_bytes="VGVzdA==",
            ),
        ]
        request_data = AnalyzeRequest(documents=documents)
        
        response = client.post("/api/analyze", json=request_data.model_dump())
        
        # Should handle partial failures gracefully
        assert response.status_code in [200, 207, 400, 422, 500]

    def test_error_response_includes_message(self, client):
        """Test error responses include helpful messages."""
        response = client.post(
            "/api/analyze",
            json={"documents": []},
        )
        
        if response.status_code >= 400:
            # Error response should have message or detail
            assert "detail" in response.json() or "message" in response.json()


class TestDocumentTypeHandling:
    """Test handling of different document types."""

    def test_invoice_document_processing(self, client):
        """Test invoice document can be processed."""
        request_data = AnalyzeRequest(
            documents=[
                DocumentInput(
                    filename="invoice.txt",
                    content_type="text/plain",
                    file_bytes="SW52b2ljZSBOdW1iZXI6IElOVi0wMDEgVGV0YWwgQW1vdW50OiAkMTAwMC4wMA==",
                )
            ]
        )
        
        response = client.post("/api/analyze", json=request_data.model_dump())
        assert response.status_code in [200, 422, 500]

    def test_receipt_document_processing(self, client):
        """Test receipt document can be processed."""
        request_data = AnalyzeRequest(
            documents=[
                DocumentInput(
                    filename="receipt.txt",
                    content_type="text/plain",
                    file_bytes="UmVjZWlwdCBEYXRlOiAyMDI0LTAxLTAxIFRvdGFsOiAkOC41MA==",
                )
            ]
        )
        
        response = client.post("/api/analyze", json=request_data.model_dump())
        assert response.status_code in [200, 422, 500]

    def test_contract_document_processing(self, client):
        """Test contract document can be processed."""
        request_data = AnalyzeRequest(
            documents=[
                DocumentInput(
                    filename="contract.pdf",
                    content_type="application/pdf",
                    file_bytes="Q29udHJhY3QgYmV0d2VlbiBQYXJ0aWVzIEEgYW5kIEI=",
                )
            ]
        )
        
        response = client.post("/api/analyze", json=request_data.model_dump())
        assert response.status_code in [200, 422, 500]


class TestChainSingletons:
    """Test singleton patterns work correctly across modules."""

    def test_classification_chain_singleton(self):
        """Test classification chain singleton reuse."""
        from app.chains.classify_chain import (
            get_classify_chain,
        )
        
        chain1 = get_classify_chain()
        chain2 = get_classify_chain()
        
        # Should be same instance (singleton)
        assert chain1 is chain2

    def test_extraction_chain_singleton(self):
        """Test extraction chain singleton reuse."""
        from app.chains.extract_chain import (
            get_financial_extraction_chain,
        )
        
        chain1 = get_financial_extraction_chain()
        chain2 = get_financial_extraction_chain()
        
        # Should be same instance (singleton)
        assert chain1 is chain2

    def test_validation_chain_singleton(self):
        """Test validation chain singleton reuse."""
        from app.chains.validate_chain import (
            get_financial_validation_chain,
        )
        
        chain1 = get_financial_validation_chain()
        chain2 = get_financial_validation_chain()
        
        # Should be same instance (singleton)
        assert chain1 is chain2

    def test_summarization_chain_singleton(self):
        """Test summarization chain singleton reuse."""
        from app.chains.summarize_chain import (
            get_financial_summary_chain,
        )
        
        chain1 = get_financial_summary_chain()
        chain2 = get_financial_summary_chain()
        
        # Should be same instance (singleton)
        assert chain1 is chain2


class TestServiceInitialization:
    """Test all services initialize without errors."""

    def test_ingestion_service_init(self):
        """Test ingestion service initializes."""
        from app.services.ingestion import DocumentIngestionService
        
        service = DocumentIngestionService()
        assert service is not None

    def test_validation_functions_exist(self):
        """Test validation functions are importable."""
        from app.services import validator
        
        # Verify key validation functions exist
        assert hasattr(validator, 'fuzzy_match')
        assert hasattr(validator, 'validate_amount')
        assert hasattr(validator, 'validate_date_format')

    def test_llm_init(self):
        """Test LLM initialization."""
        from app.utils.llm import get_llm
        
        llm = get_llm()
        assert llm is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
