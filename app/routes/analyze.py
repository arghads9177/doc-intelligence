"""
FastAPI route for document analysis endpoint.

Provides POST /api/analyze endpoint for full document processing pipeline.
"""

from fastapi import APIRouter, HTTPException, Query
from app.models.request_models import AnalyzeRequest
from app.models.output_models import AnalyzeResponse
from app.services.response_builder import build_analysis_response

# Create router
router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Analyze documents",
    description="Process documents through the complete pipeline: "
                "ingestion → classification → extraction → validation → summarization",
)
async def analyze_documents(
    request: AnalyzeRequest,
    include_summary: bool = Query(
        True,
        description="Include AI-generated summaries in response"
    ),
    include_validation: bool = Query(
        True,
        description="Include validation reports in response"
    ),
) -> AnalyzeResponse:
    """
    Analyze one or more documents through the complete pipeline.
    
    **Pipeline stages:**
    1. **Ingestion**: Extract text from PDF/image files
    2. **Classification**: Determine document type (invoice/receipt/contract)
    3. **Extraction**: Extract structured fields with confidence scores
    4. **Validation**: Validate extracted data (rule + AI layers)
    5. **Summarization**: Generate executive summary
    
    **Request body:**
    - `documents`: List of documents to analyze (required)
      - `filename`: Document filename
      - `content_type`: MIME type (e.g., 'application/pdf')
      - `file_bytes`: Base64-encoded file content
    - `include_summary`: Include summaries (default: true)
    - `include_validation`: Include validation reports (default: true)
    
    **Response:**
    JSON object with:
    - `status`: 'success', 'partial_success', or 'error'
    - `message`: Status message
    - `processed_documents`: Array of results per document
    - `total_processed`: Number of documents processed
    - `total_errors`: Number of processing failures
    - `processing_time_seconds`: Total execution time
    
    **Example request:**
    ```json
    {
      "documents": [
        {
          "filename": "invoice.pdf",
          "content_type": "application/pdf",
          "file_bytes": "JVBERi0xLjQKJ..."
        }
      ],
      "include_summary": true,
      "include_validation": true
    }
    ```
    
    **Example response:**
    ```json
    {
      "status": "success",
      "message": "Successfully processed 1 document(s)",
      "processed_documents": [
        {
          "filename": "invoice.pdf",
          "doc_type": "invoice",
          "doc_type_confidence": 0.95,
          "extracted_fields": {
            "company": {"value": "ACME Corp", "confidence": 0.95},
            "date": {"value": "2024-03-15", "confidence": 0.98},
            "total_amount": {"value": 1500.0, "confidence": 0.92},
            "currency": {"value": "USD", "confidence": 0.99}
          },
          "validation_report": {
            "is_valid": true,
            "total_issues": 0,
            "issues": [],
            "validation_confidence": 0.95
          },
          "summary": "ACME Corp invoice for $1,500 dated March 15, 2024..."
        }
      ],
      "total_processed": 1,
      "total_errors": 0,
      "processing_time_seconds": 4.23
    }
    ```
    
    Args:
        request: AnalyzeRequest with documents to process
        include_summary: Whether to generate summaries
        include_validation: Whether to include validation reports
        
    Returns:
        AnalyzeResponse with processing results
        
    Raises:
        HTTPException: If request is invalid or processing fails catastrophically
    """
    try:
        # Validate request
        if not request.documents:
            raise HTTPException(
                status_code=400,
                detail="At least one document must be provided"
            )
        
        if len(request.documents) > 100:
            raise HTTPException(
                status_code=400,
                detail="Maximum 100 documents per request"
            )
        
        # Process documents
        response = await build_analysis_response(
            request.documents,
            include_summary=include_summary,
            include_validation=include_validation,
        )
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Request processing failed: {str(e)}"
        )
