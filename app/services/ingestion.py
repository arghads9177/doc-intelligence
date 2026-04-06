"""
Ingestion service for document processing.

Handles loading documents from various sources using LangChain loaders.
Supports PDF and plain text documents via base64-encoded file content.
"""

import base64
import tempfile
import os
from typing import List
from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, PyPDFLoader

from app.models import DocumentInput


class DocumentIngestionService:
    """
    Service for ingesting documents from various formats.

    Converts base64-encoded file content into LangChain Document objects
    using appropriate loaders for different file types.
    """

    def __init__(self):
        """Initialize the ingestion service."""
        self.supported_content_types = {
            "text/plain": self._load_text_document,
            "application/pdf": self._load_pdf_document,
        }

    def ingest_document(self, document_input: DocumentInput) -> List[Document]:
        """
        Ingest a single document and return LangChain Document objects.

        Args:
            document_input: The document input containing filename, content_type, and file_bytes

        Returns:
            List[Document]: List of LangChain Document objects (usually one per document)

        Raises:
            ValueError: If content_type is not supported
            Exception: If file processing fails
        """
        if document_input.content_type not in self.supported_content_types:
            raise ValueError(
                f"Unsupported content type: {document_input.content_type}. "
                f"Supported types: {list(self.supported_content_types.keys())}"
            )

        # Decode base64 content
        try:
            file_content = base64.b64decode(document_input.file_bytes)
        except Exception as e:
            raise ValueError(f"Failed to decode base64 content: {e}")

        # Create temporary file
        file_extension = self._get_file_extension(document_input.content_type)
        with tempfile.NamedTemporaryFile(
            suffix=file_extension, delete=False
        ) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        try:
            # Load document using appropriate loader
            loader_func = self.supported_content_types[document_input.content_type]
            documents = loader_func(temp_file_path, document_input)

            # Add metadata to documents
            for doc in documents:
                if doc.metadata is None:
                    doc.metadata = {}
                doc.metadata.update({
                    "filename": document_input.filename,
                    "content_type": document_input.content_type,
                    "source": "uploaded_file",
                })
                # Add any additional metadata from input
                if document_input.metadata:
                    doc.metadata.update(document_input.metadata)

            return documents

        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass  # File may already be deleted or inaccessible

    def ingest_documents(self, document_inputs: List[DocumentInput]) -> List[Document]:
        """
        Ingest multiple documents and return all LangChain Document objects.

        Args:
            document_inputs: List of document inputs to process

        Returns:
            List[Document]: Combined list of all LangChain Document objects
        """
        all_documents = []
        for doc_input in document_inputs:
            documents = self.ingest_document(doc_input)
            all_documents.extend(documents)
        return all_documents

    def _load_text_document(self, file_path: str, document_input: DocumentInput) -> List[Document]:
        """
        Load a text document using LangChain TextLoader.

        Args:
            file_path: Path to the temporary text file
            document_input: Original document input (for context)

        Returns:
            List[Document]: List containing the loaded document
        """
        loader = TextLoader(file_path)
        documents = loader.load()
        return documents

    def _load_pdf_document(self, file_path: str, document_input: DocumentInput) -> List[Document]:
        """
        Load a PDF document using LangChain PyPDFLoader.

        Args:
            file_path: Path to the temporary PDF file
            document_input: Original document input (for context)

        Returns:
            List[Document]: List of documents (one per page)
        """
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents

    def _get_file_extension(self, content_type: str) -> str:
        """
        Get appropriate file extension for content type.

        Args:
            content_type: MIME content type

        Returns:
            str: File extension including the dot
        """
        extension_map = {
            "text/plain": ".txt",
            "application/pdf": ".pdf",
        }
        return extension_map.get(content_type, ".bin")


# Singleton instance
_ingestion_service: DocumentIngestionService | None = None


def get_ingestion_service() -> DocumentIngestionService:
    """
    Get the shared ingestion service instance (singleton pattern).

    Returns:
        DocumentIngestionService: The shared ingestion service instance
    """
    global _ingestion_service
    if _ingestion_service is None:
        _ingestion_service = DocumentIngestionService()
    return _ingestion_service


# For direct imports
ingestion_service = get_ingestion_service()
