"""
Response builder for orchestrating the document processing pipeline.

Combines ingestion, classification, extraction, validation, and summarization
into a unified response object.
"""

import time
from typing import Optional, Union
from app.models.request_models import DocumentInput
from app.models.output_models import (
    ProcessedDocument,
    AnalyzeResponse,
    ExtractedFinancial,
    ExtractedContract,
    ValidationReport,
)
from app.services.ingestion import ingestion_service
from app.chains.classify_chain import classify_document
from app.chains.extract_chain import extract_from_document
from app.chains.validate_chain import validate_document
from app.chains.summarize_chain import summarize_document


async def process_document(
    document_input: DocumentInput,
    include_summary: bool = True,
    include_validation: bool = True,
) -> tuple[ProcessedDocument, Optional[str]]:
    """
    Process a single document through the complete pipeline.
    
    Pipeline stages:
    1. Ingestion: Extract text from document
    2. Classification: Determine document type
    3. Extraction: Extract structured fields
    4. Validation: Validate extracted data
    5. Summarization: Generate summary
    
    Args:
        document_input: Input document with base64 content
        include_summary: Whether to generate summary
        include_validation: Whether to include validation report
        
    Returns:
        Tuple of (ProcessedDocument, error_message)
        error_message is None on success, string on error
    """
    try:
        # Stage 1: Ingest document
        ingested_docs = ingestion_service.ingest_document(document_input)
        if not ingested_docs:
            return (
                ProcessedDocument(
                    filename=document_input.filename,
                    doc_type="unknown",
                    doc_type_confidence=0.0,
                    validation_report=None,
                    summary=None,
                    raw_text_preview=None,
                ),
                "Failed to extract text from document",
            )
        
        # Get text content
        document_text = ingested_docs[0].page_content
        raw_preview = document_text[:500] if document_text else None
        
        # Stage 2: Classify document
        try:
            classification = classify_document(document_text)
            doc_type = classification.get("doc_type", "unknown")
            doc_type_confidence = float(classification.get("confidence", 0.0))
        except Exception as e:
            return (
                ProcessedDocument(
                    filename=document_input.filename,
                    doc_type="unknown",
                    doc_type_confidence=0.0,
                    validation_report=None,
                    summary=None,
                    raw_text_preview=raw_preview,
                ),
                f"Classification failed: {str(e)}",
            )
        
        # Handle unknown documents
        if doc_type == "unknown":
            return (
                ProcessedDocument(
                    filename=document_input.filename,
                    doc_type="unknown",
                    doc_type_confidence=doc_type_confidence,
                    validation_report=None,
                    summary=None,
                    raw_text_preview=raw_preview,
                ),
                "Document type could not be determined",
            )
        
        # Stage 3: Extract structured data
        try:
            extracted = extract_from_document(document_text, doc_type)
        except Exception as e:
            return (
                ProcessedDocument(
                    filename=document_input.filename,
                    doc_type=doc_type,
                    doc_type_confidence=doc_type_confidence,
                    validation_report=None,
                    summary=None,
                    raw_text_preview=raw_preview,
                ),
                f"Extraction failed: {str(e)}",
            )
        
        # Stage 4: Validate extracted data
        validation_report = None
        if include_validation:
            try:
                validation_report = validate_document(extracted, doc_type)
            except Exception as e:
                # Validation failure is not fatal
                validation_report = ValidationReport(
                    is_valid=False,
                    total_issues=1,
                    issues=[],
                    validation_confidence=0.0,
                )
        
        # Stage 5: Generate summary
        summary = None
        if include_summary and validation_report:
            try:
                summary = summarize_document(extracted, validation_report, doc_type)
            except Exception as e:
                summary = f"Summary generation failed: {str(e)}"
        
        # Build processed document
        processed = ProcessedDocument(
            filename=document_input.filename,
            doc_type=doc_type,
            doc_type_confidence=doc_type_confidence,
            extracted_fields=extracted.model_dump() if extracted else None,
            validation_report=validation_report,
            summary=summary,
            raw_text_preview=raw_preview,
        )
        
        return processed, None
    
    except Exception as e:
        # Catch-all for unexpected errors
        return (
            ProcessedDocument(
                filename=document_input.filename,
                doc_type="unknown",
                doc_type_confidence=0.0,
                validation_report=None,
                summary=None,
                raw_text_preview=None,
            ),
            f"Unexpected error: {str(e)}",
        )


async def build_analysis_response(
    documents: list[DocumentInput],
    include_summary: bool = True,
    include_validation: bool = True,
) -> AnalyzeResponse:
    """
    Build the complete analysis response for all documents.
    
    Args:
        documents: List of input documents to process
        include_summary: Whether to include summaries
        include_validation: Whether to include validation reports
        
    Returns:
        AnalyzeResponse with processing results
    """
    start_time = time.time()
    processed_documents = []
    total_errors = 0
    error_messages = []
    
    # Process each document
    for doc_input in documents:
        processed_doc, error = await process_document(
            doc_input,
            include_summary=include_summary,
            include_validation=include_validation,
        )
        
        processed_documents.append(processed_doc)
        
        if error:
            total_errors += 1
            error_messages.append(f"{doc_input.filename}: {error}")
    
    # Determine overall status
    if total_errors == 0:
        status = "success"
        message = f"Successfully processed {len(documents)} document(s)"
    elif total_errors < len(documents):
        status = "partial_success"
        message = f"Processed {len(documents) - total_errors}/{len(documents)} documents successfully"
    else:
        status = "error"
        message = "All documents failed to process"
    
    processing_time = time.time() - start_time
    
    return AnalyzeResponse(
        status=status,
        message=message,
        processed_documents=processed_documents,
        total_processed=len(documents),
        total_errors=total_errors,
        processing_time_seconds=processing_time,
    )
