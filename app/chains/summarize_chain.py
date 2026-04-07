"""
Summarization chains for generating document summaries.

Implements LCEL pipeline for concise, type-aware document summarization
with confidence-weighted output.
"""

from typing import Union
from langchain_core.output_parsers import StrOutputParser
from app.models.output_models import (
    ExtractedFinancial,
    ExtractedContract,
    ValidationReport,
)
from app.utils.llm import get_shared_llm
from app.prompts.summarize_prompt import get_summary_prompt


def create_financial_summary_chain():
    """
    Create LCEL summarization chain for financial documents.
    
    Returns:
        Runnable chain for financial document summarization
    """
    prompt = get_summary_prompt("invoice")
    llm = get_shared_llm()
    parser = StrOutputParser()
    
    chain = prompt | llm | parser
    return chain


def create_contract_summary_chain():
    """
    Create LCEL summarization chain for contract documents.
    
    Returns:
        Runnable chain for contract document summarization
    """
    prompt = get_summary_prompt("contract")
    llm = get_shared_llm()
    parser = StrOutputParser()
    
    chain = prompt | llm | parser
    return chain


def create_summary_chain(doc_type: str):
    """
    Create type-aware summarization chain with dynamic routing.
    
    Args:
        doc_type: Document type ('invoice', 'receipt', 'contract')
        
    Returns:
        Runnable summarization chain
        
    Raises:
        ValueError: If doc_type is not supported
    """
    doc_type_lower = str(doc_type).lower().strip()
    
    if doc_type_lower in ("invoice", "receipt"):
        return create_financial_summary_chain()
    elif doc_type_lower == "contract":
        return create_contract_summary_chain()
    else:
        raise ValueError(
            f"Unsupported document type for summarization: '{doc_type}'. "
            f"Supported types: 'invoice', 'receipt', 'contract'"
        )


# Singleton instances for chain reuse
_financial_summary_chain = None
_contract_summary_chain = None


def get_financial_summary_chain():
    """
    Get or create financial summary chain (singleton).
    
    Returns:
        Runnable financial summary chain
    """
    global _financial_summary_chain
    if _financial_summary_chain is None:
        _financial_summary_chain = create_financial_summary_chain()
    return _financial_summary_chain


def get_contract_summary_chain():
    """
    Get or create contract summary chain (singleton).
    
    Returns:
        Runnable contract summary chain
    """
    global _contract_summary_chain
    if _contract_summary_chain is None:
        _contract_summary_chain = create_contract_summary_chain()
    return _contract_summary_chain


def get_summary_chain(doc_type: str):
    """
    Get type-aware summary chain with dynamic routing (singleton).
    
    Args:
        doc_type: Document type ('invoice', 'receipt', 'contract')
        
    Returns:
        Runnable summary chain
        
    Raises:
        ValueError: If doc_type is not supported
    """
    doc_type_lower = str(doc_type).lower().strip()
    
    if doc_type_lower in ("invoice", "receipt"):
        return get_financial_summary_chain()
    elif doc_type_lower == "contract":
        return get_contract_summary_chain()
    else:
        raise ValueError(
            f"Unsupported document type for summarization: '{doc_type}'. "
            f"Supported types: 'invoice', 'receipt', 'contract'"
        )


def summarize_document(
    extracted: Union[ExtractedFinancial, ExtractedContract],
    validation: ValidationReport,
    doc_type: str,
) -> str:
    """
    Generate a summary for extracted document data.
    
    Args:
        extracted: Extracted document data
        validation: Validation report for the document
        doc_type: Document type ('invoice', 'receipt', 'contract')
        
    Returns:
        Summary string
        
    Raises:
        ValueError: If doc_type is not supported or LLM is not configured
    """
    try:
        chain = get_summary_chain(doc_type)
        
        # Format extracted data for prompt
        extracted_str = _format_extraction(extracted)
        
        # Run chain with template variables
        summary = chain.invoke({
            "extracted_data": extracted_str,
            "is_valid": validation.is_valid,
            "total_issues": validation.total_issues,
            "validation_confidence": validation.validation_confidence,
        })
        
        return summary.strip()
    
    except Exception as e:
        # Return fallback summary on error
        return f"Summary generation failed: {str(e)}"


async def asummarize_document(
    extracted: Union[ExtractedFinancial, ExtractedContract],
    validation: ValidationReport,
    doc_type: str,
) -> str:
    """
    Asynchronously generate a summary for extracted document.
    
    Args:
        extracted: Extracted document data
        validation: Validation report
        doc_type: Document type
        
    Returns:
        Summary string
    """
    try:
        chain = get_summary_chain(doc_type)
        
        extracted_str = _format_extraction(extracted)
        
        summary = await chain.ainvoke({
            "extracted_data": extracted_str,
            "is_valid": validation.is_valid,
            "total_issues": validation.total_issues,
            "validation_confidence": validation.validation_confidence,
        })
        
        return summary.strip()
    
    except Exception as e:
        return f"Async summary generation failed: {str(e)}"


def _format_extraction(extracted: Union[ExtractedFinancial, ExtractedContract]) -> str:
    """
    Format extracted data for display in summaries.
    
    Args:
        extracted: Extracted document data
        
    Returns:
        Formatted string representation
    """
    if isinstance(extracted, ExtractedFinancial):
        company = extracted.company.value if extracted.company else "Unknown"
        date = extracted.date.value if extracted.date else "Unknown date"
        amount = extracted.total_amount.value if extracted.total_amount else "Unknown"
        currency = extracted.currency.value if extracted.currency else ""
        
        # Handle items - now it's a FieldValue with value property containing the list
        items_count = 0
        if extracted.items:
            items_list = extracted.items.value if hasattr(extracted.items, 'value') else extracted.items
            items_count = len(items_list) if items_list else 0
        
        invoice_num = extracted.invoice_number.value if extracted.invoice_number else "N/A"
        
        return (
            f"Company: {company}\n"
            f"Date: {date}\n"
            f"Total Amount: {amount} {currency}\n"
            f"Item Count: {items_count}\n"
            f"Invoice/Receipt Number: {invoice_num}"
        )
    else:  # ExtractedContract
        parties = ", ".join(
            [p.value for p in (extracted.parties or [])]
        ) if extracted.parties else "Unknown"
        
        effective_date = extracted.effective_date.value if extracted.effective_date else "Unknown"
        expiration_date = extracted.expiration_date.value if extracted.expiration_date else "Ongoing"
        contract_type = extracted.contract_type.value if extracted.contract_type else "Unknown"
        
        # Handle key_obligations - now it's a FieldValue with value property containing the list
        obligations_count = 0
        if extracted.key_obligations:
            obligations_list = extracted.key_obligations.value if hasattr(extracted.key_obligations, 'value') else extracted.key_obligations
            obligations_count = len(obligations_list) if obligations_list else 0
        
        return (
            f"Parties: {parties}\n"
            f"Contract Type: {contract_type}\n"
            f"Effective Date: {effective_date}\n"
            f"Expiration Date: {expiration_date}\n"
            f"Key Obligations: {obligations_count} identified"
        )
