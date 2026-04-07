"""
Extraction prompt templates for document-type-aware field extraction.

Provides separate, specialized prompts for different document types:
- Financial documents (invoices, receipts)
- Contracts
"""

from langchain_core.prompts import ChatPromptTemplate

# ============================================================================
# FINANCIAL EXTRACTION PROMPT (Invoices, Receipts)
# ============================================================================

FINANCIAL_SYSTEM_PROMPT = """
You are an expert financial document analyzer specializing in extracting key information from invoices and receipts.

Your task is to carefully analyze the document and extract the following information with high precision:

1. **company** - The name of the company/vendor/seller issuing the document
2. **date** - The document date (issued date for invoice, transaction date for receipt)
3. **total_amount** - The total amount in the original currency (numeric value without currency symbol)
4. **currency** - The currency code (e.g., USD, EUR, GBP)
5. **items** - List of line items with descriptions and amounts (if available)
6. **invoice_number** - Invoice/receipt/transaction number/ID (if present)

For each extracted field, provide:
- The extracted value
- A confidence score (0.0-1.0) based on clarity and completeness of information
- Brief notes if there's any ambiguity or uncertainty

IMPORTANT GUIDELINES:
- Be precise with monetary amounts (preserve exact values as numeric numbers without $ or commas)
- For monetary amounts in items, extract as plain numbers (e.g., 6000.00 not $6,000.00)
- Parse dates in ISO format (YYYY-MM-DD) when possible
- For items, extract and list each line item separately with amount as numeric value
- If a field is not found or unclear, set confidence to 0.0 and note "not found" or "unclear"
- Focus on accuracy over completeness - missing fields are ok
- Do not hallucinate or guess information

Return ONLY a valid JSON object with the structure specified. No additional text.
"""

FINANCIAL_HUMAN_PROMPT = """
Extract financial information from this document:

{document_text}

Return a JSON object with fields: company, date, total_amount, currency, items (list), invoice_number.
Each field should have "value" and "confidence" (0-1).
"""

financial_extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", FINANCIAL_SYSTEM_PROMPT),
    ("human", FINANCIAL_HUMAN_PROMPT)
])

# ============================================================================
# CONTRACT EXTRACTION PROMPT (Legal Agreements)
# ============================================================================

CONTRACT_SYSTEM_PROMPT = """
You are an expert legal document analyzer specializing in extracting key information from contracts and agreements.

Your task is to carefully analyze the contract and extract the following information:

1. **parties** - List of parties involved in the contract (e.g., organizations, individuals)
2. **effective_date** - The date the contract becomes effective
3. **expiration_date** - The date the contract expires or ends (if specified)
4. **key_obligations** - Main obligations and responsibilities of each party
5. **contract_type** - Type of contract (e.g., Service Agreement, NDA, Purchase Agreement)

For each extracted field, provide:
- The extracted value
- A confidence score (0.0-1.0) based on clarity and prominence in the document
- Brief notes if there's any ambiguity or uncertainty

IMPORTANT GUIDELINES:
- Extract all parties mentioned as signatories or primary parties
- Dates should be in ISO format (YYYY-MM-DD) when possible
- Key obligations should summarize main duties and responsibilities
- Classification should reflect the primary purpose of the contract
- If a field is not found or unclear, set confidence to 0.0 and note accordingly
- Focus on material terms and key provisions
- Do not hallucinate terms - only extract what is explicitly stated

Return ONLY a valid JSON object with the structure specified. No additional text.
"""

CONTRACT_HUMAN_PROMPT = """
Extract contract information from this legal document:

{document_text}

Return a JSON object with fields: parties (list), effective_date, expiration_date, key_obligations (list), contract_type.
Each field should have "value" and "confidence" (0-1) where applicable.
"""

contract_extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", CONTRACT_SYSTEM_PROMPT),
    ("human", CONTRACT_HUMAN_PROMPT)
])

# ============================================================================
# PROMPT SELECTOR
# ============================================================================

def get_extraction_prompt(doc_type: str) -> ChatPromptTemplate:
    """
    Get the appropriate extraction prompt based on document type.
    
    Args:
        doc_type: Document type from classification ("invoice", "receipt", "contract", "unknown")
    
    Returns:
        ChatPromptTemplate: The appropriate extraction prompt
    
    Raises:
        ValueError: If doc_type is "unknown" or unsupported
    """
    if doc_type in ("invoice", "receipt"):
        return financial_extraction_prompt
    elif doc_type == "contract":
        return contract_extraction_prompt
    else:
        raise ValueError(
            f"Unsupported document type for extraction: {doc_type}. "
            f"Supported types: invoice, receipt, contract"
        )


# Export all prompts
__all__ = [
    "financial_extraction_prompt",
    "contract_extraction_prompt",
    "get_extraction_prompt",
    "FINANCIAL_SYSTEM_PROMPT",
    "FINANCIAL_HUMAN_PROMPT",
    "CONTRACT_SYSTEM_PROMPT",
    "CONTRACT_HUMAN_PROMPT",
]
