"""
Output models for the Document Intelligence API.

Pydantic schemas for structuring API responses and internal data structures.
"""

from typing import Optional, Any, Literal
from pydantic import BaseModel, Field


class FieldValue(BaseModel):
    """Represents an extracted field with confidence score."""

    value: Any = Field(..., description="The extracted value")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score (0-1)"
    )
    notes: Optional[str] = Field(
        default=None, description="Additional notes about the extraction"
    )


class ValidationIssue(BaseModel):
    """Represents a validation issue or discrepancy."""

    field: str = Field(..., description="Field name with issue")
    issue_type: str = Field(..., description="Type of issue (e.g., 'mismatch', 'missing')")
    severity: Literal["low", "medium", "high"] = Field(
        ..., description="Severity level"
    )
    detected_by: Literal["rule_layer", "ai_layer"] = Field(
        ..., description="Which validation layer detected the issue"
    )
    explanation: str = Field(..., description="Detailed explanation of the issue")
    suggested_correction: Optional[str] = Field(
        default=None, description="Suggested correction if available"
    )


class ValidationReport(BaseModel):
    """Summary of validation results for extracted document."""

    is_valid: bool = Field(..., description="Overall validation status")
    total_issues: int = Field(..., description="Number of issues found")
    issues: list[ValidationIssue] = Field(
        default_factory=list, description="List of validation issues"
    )
    validation_confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Overall validation confidence"
    )


class ExtractedFinancial(BaseModel):
    """Schema for extracted financial document data (invoices, receipts)."""

    company: Optional[FieldValue] = Field(
        default=None, description="Company or vendor name"
    )
    date: Optional[FieldValue] = Field(default=None, description="Document date")
    total_amount: Optional[FieldValue] = Field(
        default=None, description="Total amount in primary currency"
    )
    currency: Optional[FieldValue] = Field(
        default=None, description="Currency code (e.g., USD, EUR)"
    )
    items: Optional[FieldValue] = Field(
        default=None, description="Line items with amounts and descriptions"
    )
    invoice_number: Optional[FieldValue] = Field(
        default=None, description="Invoice or receipt number"
    )


class ExtractedContract(BaseModel):
    """Schema for extracted contract data."""

    parties: Optional[list[FieldValue]] = Field(
        default=None, description="Parties to the contract"
    )
    effective_date: Optional[FieldValue] = Field(
        default=None, description="Effective date of the contract"
    )
    expiration_date: Optional[FieldValue] = Field(
        default=None, description="Expiration or end date"
    )
    key_obligations: Optional[FieldValue] = Field(
        default=None, description="Key obligations from the contract"
    )
    contract_type: Optional[FieldValue] = Field(
        default=None, description="Type of contract"
    )


class ProcessedDocument(BaseModel):
    """Represents a fully processed document with all analysis."""

    filename: str = Field(..., description="Original filename")
    doc_type: Literal["invoice", "receipt", "contract", "unknown"] = Field(
        ..., description="Classified document type"
    )
    doc_type_confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence in document type classification"
    )
    extracted_fields: Optional[dict] = Field(
        default=None, description="Extracted structured data"
    )
    validation_report: Optional[ValidationReport] = Field(
        default=None, description="Validation results"
    )
    summary: Optional[str] = Field(
        default=None, description="AI-generated summary of the document"
    )
    raw_text_preview: Optional[str] = Field(
        default=None, description="First 500 characters of extracted text"
    )


class AnalyzeResponse(BaseModel):
    """Response schema for the analyze endpoint."""

    status: Literal["success", "partial_success", "error"] = Field(
        ..., description="Overall status of the analysis"
    )
    message: Optional[str] = Field(
        default=None, description="Status message or error description"
    )
    processed_documents: list[ProcessedDocument] = Field(
        ..., description="List of processed documents with analysis results"
    )
    total_processed: int = Field(
        ..., description="Total documents processed"
    )
    total_errors: int = Field(
        ..., description="Number of documents with errors"
    )
    processing_time_seconds: float = Field(
        ..., description="Total processing time in seconds"
    )
