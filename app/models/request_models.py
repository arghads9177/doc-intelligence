"""
Request models for the Document Intelligence API.

Pydantic schemas for validating incoming API requests.
"""

from typing import Optional
from pydantic import BaseModel, Field


class DocumentInput(BaseModel):
    """Schema for a single document to be processed."""

    filename: str = Field(..., description="Name of the document file")
    content_type: str = Field(
        ..., description="MIME type (e.g., 'application/pdf', 'text/plain')"
    )
    file_bytes: str = Field(
        ..., description="Base64-encoded file content"
    )
    metadata: Optional[dict] = Field(
        default=None, description="Optional metadata about the document"
    )


class AnalyzeRequest(BaseModel):
    """Schema for the main analyze endpoint request."""

    documents: list[DocumentInput] = Field(..., description="List of documents to analyze")
    include_summary: bool = Field(
        default=True, description="Whether to include summarization"
    )
    include_validation: bool = Field(
        default=True, description="Whether to include validation report"
    )
