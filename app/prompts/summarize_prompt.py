"""
Summarization prompt templates for generating document summaries.

Provides LCEL-compatible prompts for the summarization chain to generate
concise, type-aware summaries of extracted document data.
"""

from langchain_core.prompts import ChatPromptTemplate


# Financial Document Summarization Prompt
FINANCIAL_SUMMARY_SYSTEM_PROMPT = """You are an expert financial document analyst. Your job is to generate a concise, professional summary of extracted financial data.

When summarizing, focus on:

1. **Key Financial Details**:
   - Document type (invoice, receipt)
   - Vendor/company and transaction date
   - Total amount and currency
   - Main items/services provided

2. **Business Context**:
   - What goods/services were provided
   - Any special terms or conditions
   - Payment status indicators (if available)

3. **Data Quality**:
   - Note any missing critical fields
   - Flag unusual amounts or dates
   - Mention confidence issues if significant

4. **Executive Summary**:
   - Single paragraph, 2-3 sentences maximum
   - Focus on business impact, not technical details
   - Include totals in a clear format

Keep the tone professional and concise. Use financial terminology appropriately.
Avoid redundancy and focus on actionable information."""

FINANCIAL_SUMMARY_HUMAN_PROMPT = """Generate a professional summary for this financial document:

**Extracted Data:**
{extracted_data}

**Validation Status:**
Valid: {is_valid}
Issues: {total_issues}
Confidence: {validation_confidence:.0%}

Provide a 2-3 sentence executive summary that a business stakeholder would find useful. 
Include the company, date, and total amount in the summary."""


# Contract Document Summarization Prompt
CONTRACT_SUMMARY_SYSTEM_PROMPT = """You are an expert legal document analyst. Your job is to generate a clear, professional summary of extracted contract data.

When summarizing, focus on:

1. **Contract Basics**:
   - All parties involved
   - Contract type (e.g., Service Agreement, NDA)
   - Effective and expiration dates
   - Contract duration

2. **Key Terms & Obligations**:
   - Main responsibilities of each party
   - Any critical obligations or conditions
   - Payment or performance terms (if identifiable)

3. **Risk Indicators**:
   - Note any missing parties or dates
   - Flag unusual contract durations
   - Mention missing obligations if concerning

4. **Executive Summary**:
   - One paragraph maximum (3-4 sentences)
   - Focus on who, what, when structure
   - Highlight key obligations clearly

Keep the tone professional and objective. Use legal terminology appropriately.
Be concise but complete. Focus on what a legal reviewer needs to know."""

CONTRACT_SUMMARY_HUMAN_PROMPT = """Generate a professional summary for this contract:

**Extracted Data:**
{extracted_data}

**Validation Status:**
Valid: {is_valid}
Issues: {total_issues}
Confidence: {validation_confidence:.0%}

Provide a 3-4 sentence executive summary that a legal team would find useful.
Include the parties, contract type, duration, and key obligations in the summary."""


def get_financial_summary_prompt() -> ChatPromptTemplate:
    """
    Get the financial document summarization prompt template.
    
    Returns:
        ChatPromptTemplate for financial document summarization
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", FINANCIAL_SUMMARY_SYSTEM_PROMPT),
            ("human", FINANCIAL_SUMMARY_HUMAN_PROMPT),
        ]
    )


def get_contract_summary_prompt() -> ChatPromptTemplate:
    """
    Get the contract document summarization prompt template.
    
    Returns:
        ChatPromptTemplate for contract document summarization
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", CONTRACT_SUMMARY_SYSTEM_PROMPT),
            ("human", CONTRACT_SUMMARY_HUMAN_PROMPT),
        ]
    )


def get_summary_prompt(doc_type: str) -> ChatPromptTemplate:
    """
    Get type-aware summarization prompt template.
    
    Args:
        doc_type: Document type ('invoice', 'receipt', 'contract')
        
    Returns:
        ChatPromptTemplate appropriate for document type
        
    Raises:
        ValueError: If doc_type is not supported
    """
    doc_type_lower = str(doc_type).lower().strip()
    
    if doc_type_lower in ("invoice", "receipt"):
        return get_financial_summary_prompt()
    elif doc_type_lower == "contract":
        return get_contract_summary_prompt()
    else:
        raise ValueError(
            f"Unsupported document type for summarization: '{doc_type}'. "
            f"Supported types: 'invoice', 'receipt', 'contract'"
        )
