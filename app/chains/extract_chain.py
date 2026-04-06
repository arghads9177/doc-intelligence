"""
Extraction chain for document-type-aware field extraction.

LCEL pipelines that extract structured data from documents based on their type.
Supports financial documents (invoices/receipts) and contracts with confidence scoring.
"""

from typing import Union
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import Runnable, RunnablePassthrough

from app.models.output_models import ExtractedFinancial, ExtractedContract
from app.prompts.extract_prompt import get_extraction_prompt
from app.utils import get_shared_llm


def create_financial_extraction_chain() -> Runnable:
    """
    Create the financial document extraction chain using LCEL.
    
    Returns:
        Runnable: LCEL chain for extracting financial document data
    """
    try:
        llm = get_shared_llm()
    except ValueError as e:
        if "OPENAI_API_KEY" in str(e):
            raise ValueError(
                "Cannot create extraction chain: OPENAI_API_KEY not configured. "
                "Please set the API key in .env file or environment variables."
            ) from e
        raise

    prompt = get_extraction_prompt("invoice")
    parser = PydanticOutputParser(pydantic_object=ExtractedFinancial)

    # Add parser instructions to the prompt
    prompt_with_instructions = prompt.partial(
        format_instructions=parser.get_format_instructions()
    )

    # LCEL pipeline: prompt | llm | parser
    chain = prompt_with_instructions | llm | parser

    return chain


def create_contract_extraction_chain() -> Runnable:
    """
    Create the contract extraction chain using LCEL.
    
    Returns:
        Runnable: LCEL chain for extracting contract data
    """
    try:
        llm = get_shared_llm()
    except ValueError as e:
        if "OPENAI_API_KEY" in str(e):
            raise ValueError(
                "Cannot create extraction chain: OPENAI_API_KEY not configured. "
                "Please set the API key in .env file or environment variables."
            ) from e
        raise

    prompt = get_extraction_prompt("contract")
    parser = PydanticOutputParser(pydantic_object=ExtractedContract)

    # Add parser instructions to the prompt
    prompt_with_instructions = prompt.partial(
        format_instructions=parser.get_format_instructions()
    )

    # LCEL pipeline: prompt | llm | parser
    chain = prompt_with_instructions | llm | parser

    return chain


def create_extraction_chain(doc_type: str) -> Runnable:
    """
    Create a type-aware extraction chain based on document type.
    
    Args:
        doc_type: Document type ("invoice", "receipt", "contract")
    
    Returns:
        Runnable: LCEL chain for the specified document type
    
    Raises:
        ValueError: If doc_type is unsupported
    """
    if doc_type in ("invoice", "receipt"):
        return create_financial_extraction_chain()
    elif doc_type == "contract":
        return create_contract_extraction_chain()
    else:
        raise ValueError(
            f"Unsupported document type for extraction: {doc_type}. "
            f"Supported types: invoice, receipt, contract"
        )


# Singleton instances - created on first access
_financial_chain_instance: Runnable | None = None
_contract_chain_instance: Runnable | None = None


def get_financial_extraction_chain() -> Runnable:
    """
    Get the shared financial extraction chain instance (singleton pattern).
    
    Returns:
        Runnable: The shared financial extraction chain
    """
    global _financial_chain_instance
    if _financial_chain_instance is None:
        _financial_chain_instance = create_financial_extraction_chain()
    return _financial_chain_instance


def get_contract_extraction_chain() -> Runnable:
    """
    Get the shared contract extraction chain instance (singleton pattern).
    
    Returns:
        Runnable: The shared contract extraction chain
    """
    global _contract_chain_instance
    if _contract_chain_instance is None:
        _contract_chain_instance = create_contract_extraction_chain()
    return _contract_chain_instance


def get_extraction_chain(doc_type: str) -> Runnable:
    """
    Get a type-appropriate extraction chain (singleton pattern).
    
    Args:
        doc_type: Document type ("invoice", "receipt", "contract")
    
    Returns:
        Runnable: Appropriate extraction chain for the document type
    """
    if doc_type in ("invoice", "receipt"):
        return get_financial_extraction_chain()
    elif doc_type == "contract":
        return get_contract_extraction_chain()
    else:
        raise ValueError(
            f"Unsupported document type for extraction: {doc_type}. "
            f"Supported types: invoice, receipt, contract"
        )


def extract_from_document(
    document_text: str,
    doc_type: str
) -> Union[ExtractedFinancial, ExtractedContract]:
    """
    Extract structured data from a document based on its type.
    
    Args:
        document_text: The text content of the document
        doc_type: Document type classification ("invoice", "receipt", "contract")
    
    Returns:
        Union[ExtractedFinancial, ExtractedContract]: Extracted structured data
    
    Raises:
        ValueError: If doc_type is unsupported
    
    Example:
        >>> result = extract_from_document(invoice_text, "invoice")
        >>> print(result.company.value, result.company.confidence)
        "ABC Corp" 0.95
    """
    chain = get_extraction_chain(doc_type)
    result = chain.invoke({"document_text": document_text})
    return result


async def aextract_from_document(
    document_text: str,
    doc_type: str
) -> Union[ExtractedFinancial, ExtractedContract]:
    """
    Async version of extract_from_document.
    
    Args:
        document_text: The text content of the document
        doc_type: Document type classification ("invoice", "receipt", "contract")
    
    Returns:
        Union[ExtractedFinancial, ExtractedContract]: Extracted structured data
    """
    chain = get_extraction_chain(doc_type)
    result = await chain.ainvoke({"document_text": document_text})
    return result


# Export all public functions
__all__ = [
    "create_financial_extraction_chain",
    "create_contract_extraction_chain",
    "create_extraction_chain",
    "get_financial_extraction_chain",
    "get_contract_extraction_chain",
    "get_extraction_chain",
    "extract_from_document",
    "aextract_from_document",
]
