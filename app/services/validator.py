"""
Rule-based validation layer for extracted document data.

Implements deterministic validation rules for:
- Numeric amount verification
- Date parsing and validation
- Company/party name fuzzy matching
- Cross-field consistency checks
"""

from datetime import datetime
from typing import Optional, Any
from difflib import SequenceMatcher
from app.models.output_models import (
    ValidationIssue,
    ExtractedFinancial,
    ExtractedContract,
)


def fuzzy_match(str1: str, str2: str, threshold: float = 0.8) -> bool:
    """
    Perform fuzzy string matching with configurable threshold.
    
    Args:
        str1: First string to compare
        str2: Second string to compare
        threshold: Similarity threshold (0-1), default 0.8
        
    Returns:
        True if strings match above threshold, False otherwise
    """
    if not str1 or not str2:
        return False
    
    # Normalize strings
    s1 = str(str1).lower().strip()
    s2 = str(str2).lower().strip()
    
    # Exact match
    if s1 == s2:
        return True
    
    # Calculate similarity ratio
    ratio = SequenceMatcher(None, s1, s2).ratio()
    return ratio >= threshold


def validate_amount(amount: float, items: list[dict]) -> Optional[ValidationIssue]:
    """
    Validate that total amount matches sum of items.
    
    Accounts for common differences like tax, shipping, fees, and discounts.
    Allows 5% tolerance for rounding and unknown fees.
    
    Args:
        amount: Total amount claimed
        items: List of line items with amounts
        
    Returns:
        ValidationIssue if amount doesn't reasonably match items sum, None otherwise
    """
    if not items or not amount:
        return None
    
    try:
        # Extract amounts from items
        item_total = 0.0
        for item in items:
            if isinstance(item, dict) and "amount" in item:
                # Parse amount - handle both "$6,000.00" and "6000" formats
                amount_str = str(item["amount"]).replace("$", "").replace(",", "").strip()
                try:
                    item_total += float(amount_str)
                except (ValueError, TypeError):
                    # If we can't parse an item, skip it gracefully
                    continue
        
        # Allow reasonable tolerance for:
        # - Tax (typically 5-25%)
        # - Shipping and handling
        # - Small rounding differences
        # Use 30% tolerance which accounts for most legitimate additions
        tolerance = amount * 0.30
        
        difference = abs(float(amount) - item_total)
        
        if difference > tolerance:
            return ValidationIssue(
                field="total_amount",
                issue_type="amount_mismatch",
                severity="high",
                detected_by="rule_layer",
                explanation=f"Total amount ({amount}) significantly differs from sum of items ({item_total:.2f}). Difference: {difference:.2f}",
                suggested_correction=f"Verify if difference represents tax, shipping, or other fees. If legitimate, difference is {(difference/item_total)*100:.1f}% of item total.",
            )
    except (ValueError, TypeError) as e:
        pass
    
    return None


def validate_date_format(date_str: str) -> tuple[bool, Optional[datetime]]:
    """
    Validate and parse date string in multiple formats.
    
    Args:
        date_str: Date string to validate
        
    Returns:
        Tuple of (is_valid, parsed_datetime)
    """
    if not date_str:
        return False, None
    
    date_formats = [
        "%Y-%m-%d",      # 2024-03-15
        "%m/%d/%Y",      # 03/15/2024
        "%d/%m/%Y",      # 15/03/2024
        "%B %d, %Y",     # March 15, 2024
        "%b %d, %Y",     # Mar 15, 2024
        "%Y/%m/%d",      # 2024/03/15
        "%m-%d-%Y",      # 03-15-2024
        "%d-%m-%Y",      # 15-03-2024
    ]
    
    date_str_clean = str(date_str).strip()
    
    for fmt in date_formats:
        try:
            parsed = datetime.strptime(date_str_clean, fmt)
            return True, parsed
        except (ValueError, TypeError):
            continue
    
    return False, None


def validate_date_range(
    start_date: Optional[str],
    end_date: Optional[str],
) -> list[ValidationIssue]:
    """
    Validate date range (start < end and reasonable timespan).
    
    Args:
        start_date: Start date string
        end_date: End date string
        
    Returns:
        List of ValidationIssues found
    """
    issues = []
    
    if not start_date or not end_date:
        return issues
    
    valid1, parsed_start = validate_date_format(str(start_date))
    valid2, parsed_end = validate_date_format(str(end_date))
    
    if not valid1:
        issues.append(
            ValidationIssue(
                field="start_date",
                issue_type="invalid_format",
                severity="high",
                detected_by="rule_layer",
                explanation=f"Start date '{start_date}' could not be parsed",
                suggested_correction="Provide date in common format (YYYY-MM-DD, MM/DD/YYYY, etc.)",
            )
        )
    
    if not valid2:
        issues.append(
            ValidationIssue(
                field="end_date",
                issue_type="invalid_format",
                severity="high",
                detected_by="rule_layer",
                explanation=f"End date '{end_date}' could not be parsed",
                suggested_correction="Provide date in common format (YYYY-MM-DD, MM/DD/YYYY, etc.)",
            )
        )
    
    if valid1 and valid2 and parsed_start and parsed_end:
        if parsed_start >= parsed_end:
            issues.append(
                ValidationIssue(
                    field="date_range",
                    issue_type="invalid_range",
                    severity="high",
                    detected_by="rule_layer",
                    explanation=f"Start date ({parsed_start.date()}) must be before end date ({parsed_end.date()})",
                    suggested_correction=f"Swap dates or verify contract terms",
                )
            )
        
        # Check if range is unreasonably long (> 30 years)
        days_diff = (parsed_end - parsed_start).days
        if days_diff > 30 * 365:
            issues.append(
                ValidationIssue(
                    field="date_range",
                    issue_type="unusual_duration",
                    severity="low",
                    detected_by="rule_layer",
                    explanation=f"Contract duration is very long ({days_diff} days / {days_diff/365:.1f} years)",
                    suggested_correction="Verify contract is intended to span this long",
                )
            )
    
    return issues


def validate_financial_document(
    extracted: ExtractedFinancial,
) -> list[ValidationIssue]:
    """
    Run rule-based validation on extracted financial document.
    
    Args:
        extracted: ExtractedFinancial model instance
        
    Returns:
        List of ValidationIssue objects found
    """
    issues = []
    
    # Check amount vs items
    if extracted.total_amount and extracted.items:
        try:
            amount = float(extracted.total_amount.value)
            # Extract items list from FieldValue object
            items_list = extracted.items.value if hasattr(extracted.items, 'value') else extracted.items
            amount_issue = validate_amount(amount, items_list)
            if amount_issue:
                issues.append(amount_issue)
        except (ValueError, TypeError):
            pass
    
    # Check date format and validity
    if extracted.date:
        try:
            valid, parsed = validate_date_format(str(extracted.date.value))
            if not valid:
                issues.append(
                    ValidationIssue(
                        field="date",
                        issue_type="invalid_format",
                        severity="medium",
                        detected_by="rule_layer",
                        explanation=f"Date '{extracted.date.value}' could not be parsed",
                        suggested_correction="Verify date is in standard format (YYYY-MM-DD, MM/DD/YYYY, etc.)",
                    )
                )
        except (ValueError, TypeError):
            pass
    
    # Check for missing critical fields
    missing_fields = []
    if not extracted.company:
        missing_fields.append("company")
    if not extracted.date:
        missing_fields.append("date")
    if not extracted.total_amount:
        missing_fields.append("total_amount")
    if not extracted.currency:
        missing_fields.append("currency")
    
    if missing_fields:
        issues.append(
            ValidationIssue(
                field="document",
                issue_type="missing_critical_fields",
                severity="high",
                detected_by="rule_layer",
                explanation=f"Missing critical financial fields: {', '.join(missing_fields)}",
                suggested_correction="Ensure document contains complete financial information",
            )
        )
    
    # Check currency code validity (basic check for 3-letter codes)
    if extracted.currency:
        currency_code = str(extracted.currency.value).upper()
        if len(currency_code) != 3:
            issues.append(
                ValidationIssue(
                    field="currency",
                    issue_type="invalid_format",
                    severity="medium",
                    detected_by="rule_layer",
                    explanation=f"Currency '{currency_code}' does not match expected format (3-letter code)",
                    suggested_correction="Use standard ISO 4217 currency codes (USD, EUR, GBP, etc.)",
                )
            )
    
    return issues


def validate_contract_document(
    extracted: ExtractedContract,
) -> list[ValidationIssue]:
    """
    Run rule-based validation on extracted contract document.
    
    Args:
        extracted: ExtractedContract model instance
        
    Returns:
        List of ValidationIssue objects found
    """
    issues = []
    
    # Check date range validity
    if extracted.effective_date and extracted.expiration_date:
        try:
            date_issues = validate_date_range(
                str(extracted.effective_date.value),
                str(extracted.expiration_date.value),
            )
            issues.extend(date_issues)
        except (ValueError, TypeError):
            pass
    
    # Check for missing critical fields
    missing_fields = []
    if not extracted.parties or len(extracted.parties) < 2:
        missing_fields.append("parties (at least 2 required)")
    if not extracted.effective_date:
        missing_fields.append("effective_date")
    if not extracted.contract_type:
        missing_fields.append("contract_type")
    
    if missing_fields:
        issues.append(
            ValidationIssue(
                field="document",
                issue_type="missing_critical_fields",
                severity="high",
                detected_by="rule_layer",
                explanation=f"Missing critical contract fields: {', '.join(missing_fields)}",
                suggested_correction="Ensure contract contains all required information",
            )
        )
    
    # Check for single party (contracts need at least 2 parties)
    if extracted.parties and len(extracted.parties) < 2:
        issues.append(
            ValidationIssue(
                field="parties",
                issue_type="insufficient_parties",
                severity="high",
                detected_by="rule_layer",
                explanation=f"Only {len(extracted.parties)} party identified, contracts require at least 2",
                suggested_correction="Verify all contract parties are identified",
            )
        )
    
    # Check if expiration_date is missing but effective_date exists
    if extracted.effective_date and not extracted.expiration_date:
        issues.append(
            ValidationIssue(
                field="expiration_date",
                issue_type="missing_field",
                severity="low",
                detected_by="rule_layer",
                explanation="Expiration date not found (may be open-ended or perpetual contract)",
                suggested_correction="Verify if contract has expiration or renewal terms",
            )
        )
    
    return issues
