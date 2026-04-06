"""
Validation prompt templates for AI-powered semantic validation.

Provides LCEL-compatible prompts for the AI validation chain to identify
semantic issues, edge cases, and context-aware discrepancies that rule-based
validation might miss.
"""

from langchain_core.prompts import ChatPromptTemplate


# Financial Document Validation Prompt
FINANCIAL_VALIDATION_SYSTEM_PROMPT = """You are an expert financial document validator. Your job is to identify semantic issues, inconsistencies, and edge cases in extracted financial data that may indicate errors or suspicious patterns.

Analyze the extracted data for:

1. **Semantic Inconsistencies**: Do field values make sense together? (e.g., if amount is $5000, is it reasonable for a receipt vs invoice?)

2. **Pattern Analysis**: Look for unusual patterns like:
   - Suspiciously round numbers (e.g., exactly $5000.00)
   - Mismatches between company name and invoice number format
   - Dates that seem inconsistent with document type

3. **Context Issues**: 
   - Is the currency appropriate for the company location/name?
   - Are items consistent with the company type?
   - Do item descriptions suggest different document type?

4. **Extraction Quality**:
   - Do confidence scores align with data quality?
   - Are there signs of OCR errors (mixed case inconsistencies, symbol replacements)?

5. **Edge Cases**:
   - Multiple different date formats in one document?
   - Currency codes that don't match currency symbols?
   - Items without amounts in a financial document?

For each issue identified:
- Be specific about what's wrong
- Explain why it's a problem
- Suggest corrections when possible
- Rate severity appropriately

Focus on issues that would materially affect document processing or create ambiguity.
Avoid flagging minor formatting inconsistencies unless they impact understanding."""

FINANCIAL_VALIDATION_HUMAN_PROMPT = """Validate the following extracted financial document data:

Extraction Data:
{extracted_data}

Rule-Based Issues Already Detected:
{rule_issues}

Please identify any additional semantic, contextual, or edge case issues that the rule-based layer missed. Consider the confidence scores and overall data quality. Provide your analysis in this exact JSON format:

{{
  "additional_issues": [
    {{
      "field": "field_name",
      "issue_type": "type",
      "severity": "low|medium|high",
      "explanation": "Why this is a problem",
      "suggested_correction": "How to fix it"
    }}
  ],
  "overall_assessment": "Brief summary of data quality",
  "requires_human_review": true|false
}}"""


# Contract Document Validation Prompt
CONTRACT_VALIDATION_SYSTEM_PROMPT = """You are an expert legal document validator. Your job is to identify semantic issues, logical inconsistencies, and potential problems in extracted contract data.

Analyze the extracted data for:

1. **Legal Semantic Issues**:
   - Do parties match across fields (e.g., same company in "parties" and obligations)?
   - Are obligations actually obligations (action items) vs just descriptions?
   - Do contract type terms match actual content (e.g., "NDA" but no confidentiality obligations)?

2. **Date Logic**:
   - Are dates in logical order (effective before expiration)?
   - Are dates suspiciously far in the past/future?
   - Missing expiration date but type suggests it should exist (e.g., License Agreement)?

3. **Party Analysis**:
   - Are party names variations of same entity (e.g., "ACME Corp" vs "ACME Corporation")?
   - Are there enough parties for the contract type?
   - Do party roles make sense for contract type?

4. **Content Completeness**:
   - Are key obligations actually present or generic?
   - Does contract type match identified obligations?
   - Missing typical obligations for this contract type?

5. **Extraction Confidence**:
   - Do confidence scores reflect actual data quality?
   - Are low-confidence fields actually important?
   - Are high-confidence fields clearly supported in text?

6. **Red Flags**:
   - Extreme contract durations (perpetual, 1 day, etc.)?
   - Single party listed when contract type requires multiple?
   - Obligations that seem incomplete or fragmented?

Rate severity based on legal/business impact."""

CONTRACT_VALIDATION_HUMAN_PROMPT = """Validate the following extracted contract data:

Extraction Data:
{extracted_data}

Rule-Based Issues Already Detected:
{rule_issues}

Please identify any additional semantic, legal, or contextual issues that the rule-based layer missed. Consider party relationships, obligation completeness, and contract type alignment. Provide your analysis in this exact JSON format:

{{
  "additional_issues": [
    {{
      "field": "field_name",
      "issue_type": "type",
      "severity": "low|medium|high",
      "explanation": "Why this is a problem",
      "suggested_correction": "How to fix it"
    }}
  ],
  "overall_assessment": "Brief summary of contract quality and completeness",
  "requires_human_review": true|false
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
