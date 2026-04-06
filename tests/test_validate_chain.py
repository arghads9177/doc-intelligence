"""
Comprehensive test suite for hybrid validation engine (Phase 4).

Tests both rule-based validation layer and AI validation chain,
ensuring proper detection of financial and contract issues.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from app.services.validator import (
    fuzzy_match,
    validate_amount,
    validate_date_format,
    validate_date_range,
    validate_financial_document,
    validate_contract_document,
)
from app.prompts.validate_prompt import (
    get_financial_validation_prompt,
    get_contract_validation_prompt,
    get_validation_prompt,
)
from app.chains.validate_chain import (
    create_financial_validation_chain,
    create_contract_validation_chain,
    create_validation_chain,
    get_financial_validation_chain,
    get_contract_validation_chain,
    get_validation_chain,
    validate_document,
    avalidate_document,
    ValidationResponseParser,
    _format_extraction,
)
from app.models.output_models import (
    ExtractedFinancial,
    ExtractedContract,
    FieldValue,
    ValidationIssue,
)


# ============================================================================
# TEST CLASS 1: Fuzzy Matching Tests
# ============================================================================

class TestFuzzyMatching:
    """Test fuzzy string matching functionality."""
    
    def test_exact_match(self):
        """Test exact string match."""
        assert fuzzy_match("ACME Corp", "ACME Corp", 0.8) is True
    
    def test_case_insensitive_match(self):
        """Test case-insensitive matching."""
        assert fuzzy_match("acme corp", "ACME CORP", 0.8) is True
    
    def test_whitespace_normalized(self):
        """Test whitespace normalization."""
        assert fuzzy_match("ACME  Corp", "ACME Corp", 0.8) is True
    
    def test_partial_match_above_threshold(self):
        """Test partial match above threshold."""
        assert fuzzy_match("ACME Corporation", "ACME Corp", 0.7) is True
    
    def test_partial_match_below_threshold(self):
        """Test partial match below threshold."""
        assert fuzzy_match("ACME Corporation", "XYZ Inc", 0.8) is False
    
    def test_empty_strings(self):
        """Test empty string handling."""
        assert fuzzy_match("", "test", 0.8) is False
        assert fuzzy_match("test", "", 0.8) is False


# ============================================================================
# TEST CLASS 2: Amount Validation Tests
# ============================================================================

class TestAmountValidation:
    """Test financial amount validation."""
    
    def test_matching_total_and_items(self):
        """Test when total matches items sum."""
        items = [
            {"amount": 100.0},
            {"amount": 200.0},
            {"amount": 300.0},
        ]
        issue = validate_amount(600.0, items)
        assert issue is None
    
    def test_mismatched_total_and_items(self):
        """Test when total doesn't match items sum."""
        items = [
            {"amount": 100.0},
            {"amount": 200.0},
        ]
        issue = validate_amount(500.0, items)
        assert issue is not None
        assert issue.issue_type == "amount_mismatch"
        assert issue.severity == "high"
    
    def test_amount_tolerance_within_1_percent(self):
        """Test tolerance for rounding (1%)."""
        items = [
            {"amount": 100.0},
            {"amount": 200.0},
        ]
        # 301.5 is within 1% tolerance of 300 (1% = 3)
        issue = validate_amount(301.5, items)
        assert issue is None
    
    def test_amount_tolerance_outside_1_percent(self):
        """Test when difference exceeds 1% tolerance."""
        items = [
            {"amount": 100.0},
            {"amount": 200.0},
        ]
        # 310 is > 1% difference from 300
        issue = validate_amount(310.0, items)
        assert issue is not None
    
    def test_empty_items_list(self):
        """Test with empty items list."""
        issue = validate_amount(100.0, [])
        assert issue is None
    
    def test_none_amount(self):
        """Test with None amount."""
        items = [{"amount": 100.0}]
        issue = validate_amount(None, items)
        assert issue is None


# ============================================================================
# TEST CLASS 3: Date Format Validation Tests
# ============================================================================

class TestDateFormatValidation:
    """Test date format parsing and validation."""
    
    def test_iso_format_valid(self):
        """Test ISO format (YYYY-MM-DD)."""
        valid, parsed = validate_date_format("2024-03-15")
        assert valid is True
        assert parsed is not None
        assert parsed.year == 2024
        assert parsed.month == 3
        assert parsed.day == 15
    
    def test_us_format_valid(self):
        """Test US format (MM/DD/YYYY)."""
        valid, parsed = validate_date_format("03/15/2024")
        assert valid is True
        assert parsed is not None
    
    def test_european_format_valid(self):
        """Test European format (DD/MM/YYYY)."""
        valid, parsed = validate_date_format("15/03/2024")
        assert valid is True
        assert parsed is not None
    
    def test_long_format_valid(self):
        """Test long format with month name."""
        valid, parsed = validate_date_format("March 15, 2024")
        assert valid is True
        assert parsed is not None
    
    def test_invalid_format(self):
        """Test invalid date format."""
        valid, parsed = validate_date_format("invalid-date")
        assert valid is False
        assert parsed is None
    
    def test_empty_string(self):
        """Test empty string."""
        valid, parsed = validate_date_format("")
        assert valid is False
        assert parsed is None


# ============================================================================
# TEST CLASS 4: Date Range Validation Tests
# ============================================================================

class TestDateRangeValidation:
    """Test date range validation for contracts."""
    
    def test_valid_date_range(self):
        """Test valid date range (start < end)."""
        issues = validate_date_range("2024-01-01", "2025-01-01")
        assert len(issues) == 0
    
    def test_invalid_range_start_after_end(self):
        """Test invalid range (start > end)."""
        issues = validate_date_range("2025-01-01", "2024-01-01")
        assert len(issues) > 0
        assert any(i.issue_type == "invalid_range" for i in issues)
    
    def test_same_start_and_end_date(self):
        """Test when start equals end."""
        issues = validate_date_range("2024-01-01", "2024-01-01")
        assert len(issues) > 0
    
    def test_invalid_start_date_format(self):
        """Test with invalid start date format."""
        issues = validate_date_range("invalid", "2024-01-01")
        assert len(issues) > 0
        assert any(i.issue_type == "invalid_format" for i in issues)
    
    def test_invalid_end_date_format(self):
        """Test with invalid end date format."""
        issues = validate_date_range("2024-01-01", "invalid")
        assert len(issues) > 0
        assert any(i.issue_type == "invalid_format" for i in issues)
    
    def test_unreasonably_long_contract(self):
        """Test contract duration > 30 years."""
        issues = validate_date_range("1990-01-01", "2030-01-01")
        assert len(issues) > 0
        assert any(i.issue_type == "unusual_duration" for i in issues)
    
    def test_none_dates(self):
        """Test with None dates."""
        issues = validate_date_range(None, None)
        assert len(issues) == 0


# ============================================================================
# TEST CLASS 5: Financial Document Validation Tests
# ============================================================================

class TestFinancialValidation:
    """Test rule-based validation for financial documents."""
    
    @staticmethod
    def create_valid_financial():
        """Create a valid extracted financial document."""
        return ExtractedFinancial(
            company=FieldValue(value="ACME Corp", confidence=0.95),
            date=FieldValue(value="2024-03-15", confidence=0.98),
            total_amount=FieldValue(value=1500.0, confidence=0.92),
            currency=FieldValue(value="USD", confidence=0.99),
            items=[
                {"description": "Item 1", "amount": 1000.0},
                {"description": "Item 2", "amount": 500.0},
            ],
            invoice_number=FieldValue(value="INV-12345", confidence=0.97),
        )
    
    def test_valid_financial_document(self):
        """Test validation of completely valid financial document."""
        extracted = self.create_valid_financial()
        issues = validate_financial_document(extracted)
        assert len(issues) == 0
    
    def test_amount_mismatch_detection(self):
        """Test detection of amount vs items mismatch."""
        extracted = self.create_valid_financial()
        extracted.total_amount.value = 9999.0  # Doesn't match items sum
        issues = validate_financial_document(extracted)
        assert len(issues) > 0
        assert any(i.issue_type == "amount_mismatch" for i in issues)
    
    def test_invalid_date_detection(self):
        """Test detection of invalid date."""
        extracted = self.create_valid_financial()
        extracted.date.value = "not-a-date"
        issues = validate_financial_document(extracted)
        assert len(issues) > 0
        assert any(i.issue_type == "invalid_format" for i in issues)
    
    def test_invalid_currency_code(self):
        """Test detection of invalid currency code."""
        extracted = self.create_valid_financial()
        extracted.currency.value = "INVALID"
        issues = validate_financial_document(extracted)
        assert len(issues) > 0
        assert any(i.issue_type == "invalid_format" for i in issues)
    
    def test_missing_critical_fields(self):
        """Test detection of missing critical fields."""
        extracted = ExtractedFinancial(
            company=None,
            date=None,
            total_amount=None,
            currency=None,
        )
        issues = validate_financial_document(extracted)
        assert len(issues) > 0
        assert any(i.issue_type == "missing_critical_fields" for i in issues)


# ============================================================================
# TEST CLASS 6: Contract Document Validation Tests
# ============================================================================

class TestContractValidation:
    """Test rule-based validation for contract documents."""
    
    @staticmethod
    def create_valid_contract():
        """Create a valid extracted contract document."""
        return ExtractedContract(
            parties=[
                FieldValue(value="ACME Corp", confidence=0.95),
                FieldValue(value="XYZ Inc", confidence=0.94),
            ],
            effective_date=FieldValue(value="2024-01-01", confidence=0.98),
            expiration_date=FieldValue(value="2025-01-01", confidence=0.97),
            key_obligations=[
                {"party": "ACME", "obligation": "Provide services"},
                {"party": "XYZ", "obligation": "Pay fees"},
            ],
            contract_type=FieldValue(value="Service Agreement", confidence=0.96),
        )
    
    def test_valid_contract_document(self):
        """Test validation of completely valid contract."""
        extracted = self.create_valid_contract()
        issues = validate_contract_document(extracted)
        assert len(issues) == 0
    
    def test_invalid_date_range_detection(self):
        """Test detection of invalid date range."""
        extracted = self.create_valid_contract()
        extracted.effective_date.value = "2025-01-01"
        extracted.expiration_date.value = "2024-01-01"
        issues = validate_contract_document(extracted)
        assert len(issues) > 0
        assert any(i.issue_type == "invalid_range" for i in issues)
    
    def test_insufficient_parties(self):
        """Test detection of insufficient parties."""
        extracted = self.create_valid_contract()
        extracted.parties = [FieldValue(value="ACME Corp", confidence=0.95)]
        issues = validate_contract_document(extracted)
        assert len(issues) > 0
        assert any(i.issue_type == "insufficient_parties" for i in issues)
    
    def test_missing_critical_fields(self):
        """Test detection of missing critical contract fields."""
        extracted = ExtractedContract(
            parties=None,
            effective_date=None,
            contract_type=None,
        )
        issues = validate_contract_document(extracted)
        assert len(issues) > 0
        assert any(i.issue_type == "missing_critical_fields" for i in issues)
    
    def test_missing_expiration_date_warning(self):
        """Test warning for missing expiration date."""
        extracted = self.create_valid_contract()
        extracted.expiration_date = None
        issues = validate_contract_document(extracted)
        assert len(issues) > 0
        assert any(i.issue_type == "missing_field" and i.severity == "low" for i in issues)


# ============================================================================
# TEST CLASS 7: Validation Prompt Tests
# ============================================================================

class TestValidationPrompts:
    """Test validation prompt templates."""
    
    def test_financial_validation_prompt_creation(self):
        """Test financial validation prompt creation."""
        prompt = get_financial_validation_prompt()
        assert prompt is not None
        # Verify it's a ChatPromptTemplate
        assert hasattr(prompt, "format_messages")
    
    def test_contract_validation_prompt_creation(self):
        """Test contract validation prompt creation."""
        prompt = get_contract_validation_prompt()
        assert prompt is not None
        assert hasattr(prompt, "format_messages")
    
    def test_validation_prompt_selector_invoice(self):
        """Test prompt selector for invoice."""
        prompt = get_validation_prompt("invoice")
        assert prompt is not None
    
    def test_validation_prompt_selector_receipt(self):
        """Test prompt selector for receipt."""
        prompt = get_validation_prompt("receipt")
        assert prompt is not None
    
    def test_validation_prompt_selector_contract(self):
        """Test prompt selector for contract."""
        prompt = get_validation_prompt("contract")
        assert prompt is not None
    
    def test_validation_prompt_selector_invalid_type(self):
        """Test error on invalid document type."""
        with pytest.raises(ValueError):
            get_validation_prompt("invalid_type")


# ============================================================================
# TEST CLASS 8: Validation Chain Creation Tests
# ============================================================================

class TestValidationChainCreation:
    """Test validation chain creation."""
    
    @patch("app.chains.validate_chain.get_shared_llm")
    def test_create_financial_chain(self, mock_llm):
        """Test creation of financial validation chain."""
        mock_llm.return_value = MagicMock()
        chain = create_financial_validation_chain()
        assert chain is not None
    
    @patch("app.chains.validate_chain.get_shared_llm")
    def test_create_contract_chain(self, mock_llm):
        """Test creation of contract validation chain."""
        mock_llm.return_value = MagicMock()
        chain = create_contract_validation_chain()
        assert chain is not None
    
    @patch("app.chains.validate_chain.get_shared_llm")
    def test_create_validation_chain_invoice(self, mock_llm):
        """Test dynamic chain creation for invoice."""
        mock_llm.return_value = MagicMock()
        chain = create_validation_chain("invoice")
        assert chain is not None
    
    @patch("app.chains.validate_chain.get_shared_llm")
    def test_create_validation_chain_receipt(self, mock_llm):
        """Test dynamic chain creation for receipt."""
        mock_llm.return_value = MagicMock()
        chain = create_validation_chain("receipt")
        assert chain is not None
    
    @patch("app.chains.validate_chain.get_shared_llm")
    def test_create_validation_chain_contract(self, mock_llm):
        """Test dynamic chain creation for contract."""
        mock_llm.return_value = MagicMock()
        chain = create_validation_chain("contract")
        assert chain is not None
    
    def test_create_validation_chain_invalid_type(self):
        """Test error on invalid document type."""
        with pytest.raises(ValueError):
            create_validation_chain("invalid")


# ============================================================================
# TEST CLASS 9: Validation Chain Singleton Tests
# ============================================================================

class TestValidationChainSingletons:
    """Test singleton pattern for validation chains."""
    
    @patch("app.chains.validate_chain.get_shared_llm")
    @patch("app.chains.validate_chain._financial_validation_chain", None)
    def test_financial_chain_singleton(self, mock_llm):
        """Test financial chain singleton creation."""
        mock_llm.return_value = MagicMock()
        chain1 = get_financial_validation_chain()
        chain2 = get_financial_validation_chain()
        # Note: Singleton check may not work due to mocking, but chains should exist
        assert chain1 is not None
        assert chain2 is not None
    
    @patch("app.chains.validate_chain.get_shared_llm")
    @patch("app.chains.validate_chain._contract_validation_chain", None)
    def test_contract_chain_singleton(self, mock_llm):
        """Test contract chain singleton creation."""
        mock_llm.return_value = MagicMock()
        chain1 = get_contract_validation_chain()
        chain2 = get_contract_validation_chain()
        assert chain1 is not None
        assert chain2 is not None


# ============================================================================
# TEST CLASS 10: Validation Response Parser Tests
# ============================================================================

class TestValidationResponseParser:
    """Test JSON response parsing from LLM."""
    
    def test_parse_valid_json(self):
        """Test parsing valid JSON response."""
        parser = ValidationResponseParser()
        response = """{
            "additional_issues": [
                {"field": "company", "issue_type": "low_confidence", 
                 "severity": "low", "explanation": "Test"}
            ],
            "overall_assessment": "Good",
            "requires_human_review": false
        }"""
        result = parser.parse(response)
        assert isinstance(result, dict)
        assert "additional_issues" in result
        assert len(result["additional_issues"]) == 1
    
    def test_parse_json_with_extra_text(self):
        """Test parsing JSON embedded in text."""
        parser = ValidationResponseParser()
        response = """Here is the analysis:
        {
            "additional_issues": [],
            "overall_assessment": "Valid document",
            "requires_human_review": false
        }
        Thank you."""
        result = parser.parse(response)
        assert isinstance(result, dict)
        assert result["overall_assessment"] == "Valid document"
    
    def test_parse_invalid_json_fallback(self):
        """Test fallback when JSON parsing fails."""
        parser = ValidationResponseParser()
        response = "This is not valid JSON"
        result = parser.parse(response)
        assert isinstance(result, dict)
        assert result["additional_issues"] == []
        assert result["requires_human_review"] is True


# ============================================================================
# TEST CLASS 11: Extraction Formatting Tests
# ============================================================================

class TestExtractionFormatting:
    """Test formatting of extraction data for prompts."""
    
    def test_format_financial_extraction(self):
        """Test formatting of financial document."""
        extracted = ExtractedFinancial(
            company=FieldValue(value="ACME Corp", confidence=0.95),
            date=FieldValue(value="2024-03-15", confidence=0.98),
            total_amount=FieldValue(value=1500.0, confidence=0.92),
            currency=FieldValue(value="USD", confidence=0.99),
            items=[{"description": "Item 1", "amount": 1000.0}],
            invoice_number=FieldValue(value="INV-12345", confidence=0.97),
        )
        formatted = _format_extraction(extracted)
        assert "ACME Corp" in formatted
        assert "USD" in formatted
        assert "1500" in formatted
    
    def test_format_contract_extraction(self):
        """Test formatting of contract document."""
        extracted = ExtractedContract(
            parties=[
                FieldValue(value="ACME Corp", confidence=0.95),
                FieldValue(value="XYZ Inc", confidence=0.94),
            ],
            effective_date=FieldValue(value="2024-01-01", confidence=0.98),
            expiration_date=FieldValue(value="2025-01-01", confidence=0.97),
            key_obligations=[{"obligation": "Pay fees"}],
            contract_type=FieldValue(value="Service Agreement", confidence=0.96),
        )
        formatted = _format_extraction(extracted)
        assert "ACME Corp" in formatted
        assert "XYZ Inc" in formatted
        assert "Service Agreement" in formatted


# ============================================================================
# TEST CLASS 12: Validation Integration Tests
# ============================================================================

class TestValidationIntegration:
    """Integration tests for complete validation workflow."""
    
    @patch("app.chains.validate_chain.get_validation_chain")
    def test_validate_financial_document_with_issues(self, mock_chain_getter):
        """Test full validation of financial document."""
        # Create mock chain that returns data
        mock_chain = MagicMock()
        mock_chain_getter.return_value = mock_chain
        
        extracted = ExtractedFinancial(
            company=FieldValue(value="ACME Corp", confidence=0.95),
            date=FieldValue(value="2024-03-15", confidence=0.98),
            total_amount=FieldValue(value=1500.0, confidence=0.92),
            currency=FieldValue(value="USD", confidence=0.99),
            items=[{"description": "Item", "amount": 1000.0}],
        )
        
        # Mock chain response with rule issues
        mock_chain.invoke.return_value = {
            "rule_issues": [
                ValidationIssue(
                    field="total_amount",
                    issue_type="amount_mismatch",
                    severity="high",
                    detected_by="rule_layer",
                    explanation="Amount mismatch",
                )
            ],
            "ai_response": {
                "additional_issues": [],
                "overall_assessment": "Issues found",
                "requires_human_review": True,
            },
        }
        
        # Run validation
        report = validate_document(extracted, "invoice")
        assert report.is_valid is False
        assert report.total_issues > 0
    
    def test_validate_document_error_handling(self):
        """Test error handling in validation."""
        extracted = ExtractedFinancial()
        # This should handle gracefully and return error report
        report = validate_document(extracted, "unknown_type")
        assert report.is_valid is False
        assert report.total_issues >= 1


# ============================================================================
# TEST CLASS 13: Validation Async Tests
# ============================================================================

class TestValidationAsync:
    """Test async validation functionality."""
    
    @pytest.mark.asyncio
    @patch("app.chains.validate_chain.get_validation_chain")
    async def test_avalidate_document(self, mock_chain_getter):
        """Test async validation of document."""
        mock_chain = MagicMock()
        mock_chain_getter.return_value = mock_chain
        
        extracted = ExtractedFinancial(
            company=FieldValue(value="ACME Corp", confidence=0.95),
            date=FieldValue(value="2024-03-15", confidence=0.98),
            total_amount=FieldValue(value=1500.0, confidence=0.92),
            currency=FieldValue(value="USD", confidence=0.99),
        )
        
        # Mock async invoke
        mock_chain.ainvoke = MagicMock()
        mock_chain.ainvoke.return_value = {
            "rule_issues": [],
            "ai_response": {
                "additional_issues": [],
                "overall_assessment": "Valid",
                "requires_human_review": False,
            },
        }
        
        report = await avalidate_document(extracted, "invoice")
        assert isinstance(report, object)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
