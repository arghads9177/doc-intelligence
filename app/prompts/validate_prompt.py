"""
Validation prompt templates for AI-powered semantic validation.

Provides LCEL-compatible prompts for the AI validation chain to identify
critical semantic issues that rule-based validation might miss.
"""

from langchain_core.prompts import ChatPromptTemplate


# Financial Document Validation Prompt
FINANCIAL_VALIDATION_SYSTEM_PROMPT = """You are a financial data validator. Return NO ISSUES unless proven wrong.

RETURN EMPTY ISSUES LIST IF:
- All amounts are positive
- Currency code exists and is valid (USD, EUR, GBP, etc.)
- Dates can be parsed
- Item totals approximately match document total (within 30% for tax/fees)
- No internal contradictions

ONLY flag if truly impossible:
- Negative amount when should be positive
- Missing absolutely required field (no date, no total, etc)
- Internal contradiction proving data is wrong

Do NOT flag:
- Format variations ($5000 vs 5000.00)
- Currency code/symbol pairs (USD=$ is standard)
- Round numbers or unusual values
- Date format differences

Return: empty additional_issues list in most cases."""

FINANCIAL_VALIDATION_HUMAN_PROMPT = """Validate this financial data format:

{extracted_data}

Rule validation already found:
{rule_issues}

Return JSON. In most cases, return empty additional_issues unless you find proven errors:
{{
  "additional_issues": [],
  "overall_assessment": "Valid" or "Has issues",
  "requires_human_review": false
}}

FAIL ONLY IF: proven impossible values or internal contradictions."""


# Contract Document Validation Prompt
CONTRACT_VALIDATION_SYSTEM_PROMPT = """Validate contract data. Return empty issues unless proven critical error.

Only flag:
- Party names contradict each other
- Expiration date before effective date
- Missing absolutely essential field

Ignore format/style variations."""

CONTRACT_VALIDATION_HUMAN_PROMPT = """Validate contract data:

{extracted_data}

Rule results:
{rule_issues}

Return JSON:
{{
  "additional_issues": [],
  "overall_assessment": "Valid or Invalid",
  "requires_human_review": false
}}"""


def get_financial_validation_prompt() -> ChatPromptTemplate:
    """
    Get the financial document validation prompt template.
    
    Returns:
        ChatPromptTemplate for financial document validation
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", FINANCIAL_VALIDATION_SYSTEM_PROMPT),
            ("human", FINANCIAL_VALIDATION_HUMAN_PROMPT),
        ]
    )


def get_contract_validation_prompt() -> ChatPromptTemplate:
    """
    Get the contract document validation prompt template.
    
    Returns:
        ChatPromptTemplate for contract document validation
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", CONTRACT_VALIDATION_SYSTEM_PROMPT),
            ("human", CONTRACT_VALIDATION_HUMAN_PROMPT),
        ]
    )


def get_validation_prompt(doc_type: str) -> ChatPromptTemplate:
    """
    Get type-aware validation prompt template.
    
    Args:
        doc_type: Document type ('invoice', 'receipt', 'contract')
        
    Returns:
        ChatPromptTemplate appropriate for document type
        
    Raises:
        ValueError: If doc_type is not supported
    """
    doc_type_lower = str(doc_type).lower().strip()
    
    if doc_type_lower in ("invoice", "receipt"):
        return get_financial_validation_prompt()
    elif doc_type_lower == "contract":
        return get_contract_validation_prompt()
    else:
        raise ValueError(
            f"Unsupported document type for validation: '{doc_type}'. "
            f"Supported types: 'invoice', 'receipt', 'contract'"
        )
