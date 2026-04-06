"""
Tests for the document ingestion service.
"""

import base64
import pytest
from unittest.mock import patch, MagicMock

from app.models import DocumentInput
from app.services.ingestion import DocumentIngestionService, get_ingestion_service


class TestDocumentIngestionService:
    """Test cases for DocumentIngestionService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = DocumentIngestionService()
        self.sample_text = "This is a test document.\nIt contains multiple lines."
        self.sample_pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n"

    def test_supported_content_types(self):
        """Test that supported content types are correctly defined."""
        expected_types = {"text/plain", "application/pdf"}
        assert set(self.service.supported_content_types.keys()) == expected_types

    def test_get_file_extension(self):
        """Test file extension mapping."""
        assert self.service._get_file_extension("text/plain") == ".txt"
        assert self.service._get_file_extension("application/pdf") == ".pdf"
        assert self.service._get_file_extension("unknown/type") == ".bin"

    def test_ingest_text_document(self):
        """Test ingesting a text document."""
        # Encode text as base64
        encoded_content = base64.b64encode(self.sample_text.encode()).decode()

        doc_input = DocumentInput(
            filename="test.txt",
            content_type="text/plain",
            file_bytes=encoded_content
        )

        documents = self.service.ingest_document(doc_input)

        assert len(documents) == 1
        assert documents[0].page_content == self.sample_text
        assert documents[0].metadata["filename"] == "test.txt"
        assert documents[0].metadata["content_type"] == "text/plain"

    def test_ingest_pdf_document(self):
        """Test ingesting a PDF document."""
        # Create a simple valid PDF content (minimal PDF)
        pdf_content = (
            b"%PDF-1.4\n"
            b"1 0 obj\n"
            b"<<\n"
            b"/Type /Catalog\n"
            b"/Pages 2 0 R\n"
            b">>\n"
            b"endobj\n"
            b"2 0 obj\n"
            b"<<\n"
            b"/Type /Pages\n"
            b"/Kids [3 0 R]\n"
            b"/Count 1\n"
            b">>\n"
            b"endobj\n"
            b"3 0 obj\n"
            b"<<\n"
            b"/Type /Page\n"
            b"/Parent 2 0 R\n"
            b"/MediaBox [0 0 612 792]\n"
            b"/Contents 4 0 R\n"
            b"/Resources <<\n"
            b"/Font <<\n"
            b"/F1 5 0 R\n"
            b">>\n"
            b">>\n"
            b">>\n"
            b"endobj\n"
            b"4 0 obj\n"
            b"<<\n"
            b"/Length 44\n"
            b">>\n"
            b"stream\n"
            b"BT\n"
            b"/F1 12 Tf\n"
            b"100 700 Td\n"
            b"(Test PDF Content) Tj\n"
            b"ET\n"
            b"endstream\n"
            b"endobj\n"
            b"5 0 obj\n"
            b"<<\n"
            b"/Type /Font\n"
            b"/Subtype /Type1\n"
            b"/BaseFont /Helvetica\n"
            b">>\n"
            b"endobj\n"
            b"xref\n"
            b"0 6\n"
            b"0000000000 65535 f \n"
            b"0000000009 00000 n \n"
            b"0000000058 00000 n \n"
            b"0000000115 00000 n \n"
            b"0000000274 00000 n \n"
            b"0000000416 00000 n \n"
            b"trailer\n"
            b"<<\n"
            b"/Size 6\n"
            b"/Root 1 0 R\n"
            b">>\n"
            b"startxref\n"
            b"477\n"
            b"%%EOF\n"
        )

        encoded_content = base64.b64encode(pdf_content).decode()

        doc_input = DocumentInput(
            filename="test.pdf",
            content_type="application/pdf",
            file_bytes=encoded_content
        )

        documents = self.service.ingest_document(doc_input)

        # PDF loader may return multiple pages or split content
        assert len(documents) >= 1
        assert documents[0].metadata["filename"] == "test.pdf"
        assert documents[0].metadata["content_type"] == "application/pdf"
        # Check that some text was extracted
        assert "Test PDF Content" in documents[0].page_content

    def test_ingest_multiple_documents(self):
        """Test ingesting multiple documents."""
        text_doc = DocumentInput(
            filename="test1.txt",
            content_type="text/plain",
            file_bytes=base64.b64encode(b"Text content").decode()
        )

        # Use valid PDF content
        pdf_content = (
            b"%PDF-1.4\n"
            b"1 0 obj\n"
            b"<<\n"
            b"/Type /Catalog\n"
            b"/Pages 2 0 R\n"
            b">>\n"
            b"endobj\n"
            b"2 0 obj\n"
            b"<<\n"
            b"/Type /Pages\n"
            b"/Kids [3 0 R]\n"
            b"/Count 1\n"
            b">>\n"
            b"endobj\n"
            b"3 0 obj\n"
            b"<<\n"
            b"/Type /Page\n"
            b"/Parent 2 0 R\n"
            b"/MediaBox [0 0 612 792]\n"
            b"/Contents 4 0 R\n"
            b"/Resources <<\n"
            b"/Font <<\n"
            b"/F1 5 0 R\n"
            b">>\n"
            b">>\n"
            b">>\n"
            b"endobj\n"
            b"4 0 obj\n"
            b"<<\n"
            b"/Length 44\n"
            b">>\n"
            b"stream\n"
            b"BT\n"
            b"/F1 12 Tf\n"
            b"100 700 Td\n"
            b"(PDF Content) Tj\n"
            b"ET\n"
            b"endstream\n"
            b"endobj\n"
            b"5 0 obj\n"
            b"<<\n"
            b"/Type /Font\n"
            b"/Subtype /Type1\n"
            b"/BaseFont /Helvetica\n"
            b">>\n"
            b"endobj\n"
            b"xref\n"
            b"0 6\n"
            b"0000000000 65535 f \n"
            b"0000000009 00000 n \n"
            b"0000000058 00000 n \n"
            b"0000000115 00000 n \n"
            b"0000000274 00000 n \n"
            b"0000000416 00000 n \n"
            b"trailer\n"
            b"<<\n"
            b"/Size 6\n"
            b"/Root 1 0 R\n"
            b">>\n"
            b"startxref\n"
            b"477\n"
            b"%%EOF\n"
        )

        pdf_doc = DocumentInput(
            filename="test2.pdf",
            content_type="application/pdf",
            file_bytes=base64.b64encode(pdf_content).decode()
        )

        documents = self.service.ingest_documents([text_doc, pdf_doc])

        assert len(documents) >= 2  # PDF might split into multiple docs

        # Check filenames are preserved
        filenames = {doc.metadata["filename"] for doc in documents}
        assert "test1.txt" in filenames
        assert "test2.pdf" in filenames

    def test_unsupported_content_type(self):
        """Test error handling for unsupported content types."""
        doc_input = DocumentInput(
            filename="test.docx",
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            file_bytes=base64.b64encode(b"fake content").decode()
        )

        with pytest.raises(ValueError, match="Unsupported content type"):
            self.service.ingest_document(doc_input)

    def test_invalid_base64(self):
        """Test error handling for invalid base64 content."""
        doc_input = DocumentInput(
            filename="test.txt",
            content_type="text/plain",
            file_bytes="invalid-base64!"
        )

        with pytest.raises(ValueError, match="Failed to decode base64 content"):
            self.service.ingest_document(doc_input)

    def test_metadata_preservation(self):
        """Test that custom metadata is preserved."""
        custom_metadata = {"source": "test", "priority": "high"}

        doc_input = DocumentInput(
            filename="test.txt",
            content_type="text/plain",
            file_bytes=base64.b64encode(b"content").decode(),
            metadata=custom_metadata
        )

        documents = self.service.ingest_document(doc_input)

        assert documents[0].metadata["source"] == "test"
        assert documents[0].metadata["priority"] == "high"
        assert documents[0].metadata["filename"] == "test.txt"


class TestIngestionServiceSingleton:
    """Test the singleton pattern for ingestion service."""

    def test_singleton_pattern(self):
        """Test that get_ingestion_service returns the same instance."""
        service1 = get_ingestion_service()
        service2 = get_ingestion_service()

        assert service1 is service2
        assert isinstance(service1, DocumentIngestionService)
