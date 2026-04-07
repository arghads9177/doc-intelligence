"""
AI-powered validation chain for hybrid validation engine.

Implements LCEL pipeline that combines rule-based validation (deterministic checks)
with AI validation (semantic analysis) to produce comprehensive ValidationReport.

Pipeline:
1. Run rule-based validation
2. Format rule issues
3. Send to LLM with context
4. Parse LLM response for additional issues
5. Combine all issues into ValidationReport
"""

import json
from typing import Union, Optional
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from app.models.output_models import (
    ExtractedFinancial,
    ExtractedContract,
    ValidationReport,
    ValidationIssue,
)
from app.utils.llm import get_shared_llm
from app.services.validator import (
    validate_financial_document,
    validate_contract_document,
)
from app.prompts.validate_prompt import get_validation_prompt


class ValidationResponseParser(BaseOutputParser):
    """Parse LLM validation response JSON into additional issues."""
    
    def parse(self, text: str) -> dict:
        """
        Parse JSON response from validation LLM.
        
        Args:
            text: JSON response from LLM
            
        Returns:
            Dictionary with 'additional_issues', 'overall_assessment', 'requires_human_review'
        """
        try:
            # Extract JSON from response
            json_start = text.find("{")
            json_end = text.rfind("}") + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = text[json_start:json_end]
                parsed = json.loads(json_str)
                
                return {
                    "additional_issues": parsed.get("additional_issues", []),
                    "overall_assessment": parsed.get("overall_assessment", ""),
                    "requires_human_review": parsed.get("requires_human_review", False),
                }
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Fallback if JSON parsing fails
        return {
            "additional_issues": [],
            "overall_assessment": "Could not parse AI response",
            "requires_human_review": True,
        }


def create_financial_validation_chain():
    """
    Create LCEL validation chain for financial documents.
    
    Returns:
        Runnable chain for financial document validation
    """
    
    def validate_step(extracted: ExtractedFinancial):
        """Run rule-based validation on financial document."""
        issues = validate_financial_document(extracted)
        return {
            "extracted": extracted,
            "rule_issues": issues,
        }
    
    def format_rule_issues(data: dict) -> str:
        """Format rule issues for LLM context."""
        issues = data["rule_issues"]
        if not issues:
            return "No rule-based issues detected"
        
        formatted = []
        for issue in issues:
            formatted.append(
                f"- {issue.field}: {issue.issue_type} ({issue.severity}) - {issue.explanation}"
            )
        return "\n".join(formatted)
    
    # Get prompt and LLM
    prompt = get_validation_prompt("invoice")
    llm = get_shared_llm()
    parser = ValidationResponseParser()
    
    # Build chain
    rule_validation = RunnableLambda(validate_step)
    prompt_chain = prompt.partial(
        extracted_data=RunnableLambda(lambda x: _format_extraction(x["extracted"])),
        rule_issues=RunnableLambda(format_rule_issues),
    )
    
    chain = (
        rule_validation
        | RunnablePassthrough.assign(
            ai_response=prompt_chain | llm | parser
        )
    )
    
    return chain


def create_contract_validation_chain():
    """
    Create LCEL validation chain for contract documents.
    
    Returns:
        Runnable chain for contract document validation
    """
    
    def validate_step(extracted: ExtractedContract):
        """Run rule-based validation on contract document."""
        issues = validate_contract_document(extracted)
        return {
            "extracted": extracted,
            "rule_issues": issues,
        }
    
    def format_rule_issues(data: dict) -> str:
        """Format rule issues for LLM context."""
        issues = data["rule_issues"]
        if not issues:
            return "No rule-based issues detected"
        
        formatted = []
        for issue in issues:
            formatted.append(
                f"- {issue.field}: {issue.issue_type} ({issue.severity}) - {issue.explanation}"
            )
        return "\n".join(formatted)
    
    # Get prompt and LLM
    prompt = get_validation_prompt("contract")
    llm = get_shared_llm()
    parser = ValidationResponseParser()
    
    # Build chain
    rule_validation = RunnableLambda(validate_step)
    prompt_chain = prompt.partial(
        extracted_data=RunnableLambda(lambda x: _format_extraction(x["extracted"])),
        rule_issues=RunnableLambda(format_rule_issues),
    )
    
    chain = (
        rule_validation
        | RunnablePassthrough.assign(
            ai_response=prompt_chain | llm | parser
        )
    )
    
    return chain


def create_validation_chain(doc_type: str):
    """
    Create type-aware validation chain with dynamic routing.
    
    Args:
        doc_type: Document type ('invoice', 'receipt', 'contract')
        
    Returns:
        Runnable validation chain
        
    Raises:
        ValueError: If doc_type is not supported
    """
    doc_type_lower = str(doc_type).lower().strip()
    
    if doc_type_lower in ("invoice", "receipt"):
        return create_financial_validation_chain()
    elif doc_type_lower == "contract":
        return create_contract_validation_chain()
    else:
        raise ValueError(
            f"Unsupported document type for validation: '{doc_type}'. "
            f"Supported types: 'invoice', 'receipt', 'contract'"
        )


# Singleton instances for chain reuse
_financial_validation_chain = None
_contract_validation_chain = None


def get_financial_validation_chain():
    """
    Get or create financial validation chain (singleton).
    
    Returns:
        Runnable financial validation chain
    """
    global _financial_validation_chain
    if _financial_validation_chain is None:
        _financial_validation_chain = create_financial_validation_chain()
    return _financial_validation_chain


def get_contract_validation_chain():
    """
    Get or create contract validation chain (singleton).
    
    Returns:
        Runnable contract validation chain
    """
    global _contract_validation_chain
    if _contract_validation_chain is None:
        _contract_validation_chain = create_contract_validation_chain()
    return _contract_validation_chain


def get_validation_chain(doc_type: str):
    """
    Get type-aware validation chain with dynamic routing (singleton).
    
    Args:
        doc_type: Document type ('invoice', 'receipt', 'contract')
        
    Returns:
        Runnable validation chain
        
    Raises:
        ValueError: If doc_type is not supported
    """
    doc_type_lower = str(doc_type).lower().strip()
    
    if doc_type_lower in ("invoice", "receipt"):
        return get_financial_validation_chain()
    elif doc_type_lower == "contract":
        return get_contract_validation_chain()
    else:
        raise ValueError(
            f"Unsupported document type for validation: '{doc_type}'. "
            f"Supported types: 'invoice', 'receipt', 'contract'"
        )


def validate_document(
    extracted: Union[ExtractedFinancial, ExtractedContract],
    doc_type: str,
) -> ValidationReport:
    """
    Validate extracted document with hybrid rule + AI validation.
    
    Runs both rule-based deterministic checks and AI semantic validation,
    combining results into comprehensive ValidationReport.
    
    Args:
        extracted: Extracted document data (ExtractedFinancial or ExtractedContract)
        doc_type: Document type ('invoice', 'receipt', 'contract')
        
    Returns:
        ValidationReport with all issues and overall assessment
        
    Raises:
        ValueError: If doc_type is not supported or LLM is not configured
    """
    try:
        chain = get_validation_chain(doc_type)
        result = chain.invoke(extracted)
        
        # Combine rule and AI issues
        all_issues = []
        
        # Add rule-based issues
        if "rule_issues" in result:
            all_issues.extend(result["rule_issues"])
        
        # Add AI-detected issues
        if "ai_response" in result:
            ai_issues = result["ai_response"].get("additional_issues", [])
            for issue_data in ai_issues:
                try:
                    issue = ValidationIssue(
                        field=issue_data.get("field", "unknown"),
                        issue_type=issue_data.get("issue_type", "unknown"),
                        severity=issue_data.get("severity", "low"),
                        detected_by="ai_layer",
                        explanation=issue_data.get("explanation", ""),
                        suggested_correction=issue_data.get("suggested_correction"),
                    )
                    all_issues.append(issue)
                except (ValueError, KeyError):
                    pass
        
        # Count by severity
        high_severity = len([i for i in all_issues if i.severity == "high"])
        
        # Determine overall validity
        is_valid = high_severity == 0
        
        # Calculate validation confidence
        # Higher confidence if fewer issues, especially high-severity ones
        if not all_issues:
            validation_confidence = 0.95
        else:
            base_confidence = max(0.5, 1.0 - (len(all_issues) * 0.1))
            severity_penalty = high_severity * 0.15
            validation_confidence = max(0.1, base_confidence - severity_penalty)
        
        return ValidationReport(
            is_valid=is_valid,
            total_issues=len(all_issues),
            issues=all_issues,
            validation_confidence=validation_confidence,
        )
    
    except Exception as e:
        # Return error report if validation fails
        return ValidationReport(
            is_valid=False,
            total_issues=1,
            issues=[
                ValidationIssue(
                    field="validation",
                    issue_type="validation_error",
                    severity="high",
                    detected_by="rule_layer",
                    explanation=f"Validation process failed: {str(e)}",
                    suggested_correction="Check document and try again",
                )
            ],
            validation_confidence=0.0,
        )


async def avalidate_document(
    extracted: Union[ExtractedFinancial, ExtractedContract],
    doc_type: str,
) -> ValidationReport:
    """
    Asynchronously validate extracted document with hybrid validation.
    
    Args:
        extracted: Extracted document data
        doc_type: Document type ('invoice', 'receipt', 'contract')
        
    Returns:
        ValidationReport with all issues and assessment
    """
    # For async, we use ainvoke on the chain
    try:
        chain = get_validation_chain(doc_type)
        result = await chain.ainvoke(extracted)
        
        # Combine issues (same logic as sync version)
        all_issues = []
        
        if "rule_issues" in result:
            all_issues.extend(result["rule_issues"])
        
        if "ai_response" in result:
            ai_issues = result["ai_response"].get("additional_issues", [])
            for issue_data in ai_issues:
                try:
                    issue = ValidationIssue(
                        field=issue_data.get("field", "unknown"),
                        issue_type=issue_data.get("issue_type", "unknown"),
                        severity=issue_data.get("severity", "low"),
                        detected_by="ai_layer",
                        explanation=issue_data.get("explanation", ""),
                        suggested_correction=issue_data.get("suggested_correction"),
                    )
                    all_issues.append(issue)
                except (ValueError, KeyError):
                    pass
        
        high_severity = len([i for i in all_issues if i.severity == "high"])
        is_valid = high_severity == 0
        
        if not all_issues:
            validation_confidence = 0.95
        else:
            base_confidence = max(0.5, 1.0 - (len(all_issues) * 0.1))
            severity_penalty = high_severity * 0.15
            validation_confidence = max(0.1, base_confidence - severity_penalty)
        
        return ValidationReport(
            is_valid=is_valid,
            total_issues=len(all_issues),
            issues=all_issues,
            validation_confidence=validation_confidence,
        )
    
    except Exception as e:
        return ValidationReport(
            is_valid=False,
            total_issues=1,
            issues=[
                ValidationIssue(
                    field="validation",
                    issue_type="validation_error",
                    severity="high",
                    detected_by="rule_layer",
                    explanation=f"Async validation failed: {str(e)}",
                    suggested_correction="Check document and try again",
                )
            ],
            validation_confidence=0.0,
        )


def _format_extraction(extracted: Union[ExtractedFinancial, ExtractedContract]) -> str:
    """
    Format extracted data for display in prompts.
    
    Args:
        extracted: Extracted document data
        
    Returns:
        Formatted string representation
    """
    if isinstance(extracted, ExtractedFinancial):
        # Handle items - now it's a FieldValue with value property containing the list
        items_count = 0
        if extracted.items:
            items_list = extracted.items.value if hasattr(extracted.items, 'value') else extracted.items
            items_count = len(items_list) if items_list else 0
        
        return (
            f"Company: {extracted.company.value if extracted.company else 'N/A'} "
            f"(confidence: {extracted.company.confidence if extracted.company else 'N/A'})\n"
            f"Date: {extracted.date.value if extracted.date else 'N/A'} "
            f"(confidence: {extracted.date.confidence if extracted.date else 'N/A'})\n"
            f"Total Amount: {extracted.total_amount.value if extracted.total_amount else 'N/A'} "
            f"{extracted.currency.value if extracted.currency else ''} "
            f"(confidence: {extracted.total_amount.confidence if extracted.total_amount else 'N/A'})\n"
            f"Items: {items_count} line items\n"
            f"Invoice Number: {extracted.invoice_number.value if extracted.invoice_number else 'N/A'} "
            f"(confidence: {extracted.invoice_number.confidence if extracted.invoice_number else 'N/A'})"
        )
    else:  # ExtractedContract
        parties_str = ", ".join(
            [p.value for p in (extracted.parties or [])]
        ) if extracted.parties else "N/A"
        
        # Handle key_obligations - now it's a FieldValue with value property containing the list
        obligations_count = 0
        if extracted.key_obligations:
            obligations_list = extracted.key_obligations.value if hasattr(extracted.key_obligations, 'value') else extracted.key_obligations
            obligations_count = len(obligations_list) if obligations_list else 0
        
        return (
            f"Parties: {parties_str}\n"
            f"Effective Date: {extracted.effective_date.value if extracted.effective_date else 'N/A'} "
            f"(confidence: {extracted.effective_date.confidence if extracted.effective_date else 'N/A'})\n"
            f"Expiration Date: {extracted.expiration_date.value if extracted.expiration_date else 'N/A'} "
            f"(confidence: {extracted.expiration_date.confidence if extracted.expiration_date else 'N/A'})\n"
            f"Contract Type: {extracted.contract_type.value if extracted.contract_type else 'N/A'} "
            f"(confidence: {extracted.contract_type.confidence if extracted.contract_type else 'N/A'})\n"
            f"Key Obligations: {obligations_count} items"
        )
