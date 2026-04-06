"""
Tests for the document extraction chains.
"""

import pytest
from unittest.mock import patch, MagicMock

from app.chains.extract_chain import (
    create_financial_extraction_chain,
    create_contract_extraction_chain,
    create_extraction_chain,
    get_financial_extraction_chain,
    get_contract_extraction_chain,
    get_extraction_chain,
    extract_from_document,
)
from app.models.output_models import ExtractedFinancial, ExtractedContract
from app.prompts.extract_prompt import get_extraction_prompt


class TestExtractionPromptSelector:
    """Test the extraction prompt selection logic."""

    def test_get_financial_prompt_for_invoice(self):
        """Test getting financial prompt for invoice."""
        prompt = get_extraction_prompt("invoice")
        assert prompt is not None
        assert len(prompt.messages) == 2  # System + human

    def test_get_financial_prompt_for_receipt(self):
        """Test getting financial prompt for receipt."""
        prompt = get_extraction_prompt("receipt")
        assert prompt is not None
        assert len(prompt.messages) == 2

    def test_get_contract_prompt(self):
        """Test getting contract prompt."""
        prompt = get_extraction_prompt("contract")
        assert prompt is not None
        assert len(prompt.messages) == 2

    def test_unsupported_document_type(self):
        """Test error for unsupported document type."""
        with pytest.raises(ValueError, match="Unsupported document type"):
            get_extraction_prompt("unknown")

    def test_financial_prompt_content(self):
        """Test that financial prompt contains key instructions."""
        prompt = get_extraction_prompt("invoice")
        prompt_str = str(prompt)
        assert "company" in prompt_str.lower()
        assert "amount" in prompt_str.lower()
        assert "currency" in prompt_str.lower()

    def test_contract_prompt_content(self):
        """Test that contract prompt contains key instructions."""
        prompt = get_extraction_prompt("contract")
        prompt_str = str(prompt)
        assert "parties" in prompt_str.lower()
        assert "effective_date" in prompt_str.lower()
        assert "obligations" in prompt_str.lower()


class TestExtractionChainCreation:
    """Test creation of extraction chains."""

    def setup_method(self):
        """Reset singleton instances before each test."""
        import app.chains.extract_chain
        app.chains.extract_chain._financial_chain_instance = None
        app.chains.extract_chain._contract_chain_instance = None

    @patch('app.chains.extract_chain.get_shared_llm')
    def test_create_financial_extraction_chain(self, mock_get_llm):
        """Test creating financial extraction chain."""
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        chain = create_financial_extraction_chain()
        assert chain is not None
        assert hasattr(chain, 'invoke')

    @patch('app.chains.extract_chain.get_shared_llm')
    def test_create_contract_extraction_chain(self, mock_get_llm):
        """Test creating contract extraction chain."""
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        chain = create_contract_extraction_chain()
        assert chain is not None
        assert hasattr(chain, 'invoke')

    @patch('app.chains.extract_chain.get_shared_llm')
    def test_create_extraction_chain_for_invoice(self, mock_get_llm):
        """Test creating extraction chain for invoice."""
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        chain = create_extraction_chain("invoice")
        assert chain is not None

    @patch('app.chains.extract_chain.get_shared_llm')
    def test_create_extraction_chain_for_receipt(self, mock_get_llm):
        """Test creating extraction chain for receipt."""
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        chain = create_extraction_chain("receipt")
        assert chain is not None

    @patch('app.chains.extract_chain.get_shared_llm')
    def test_create_extraction_chain_for_contract(self, mock_get_llm):
        """Test creating extraction chain for contract."""
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        chain = create_extraction_chain("contract")
        assert chain is not None

    @patch('app.chains.extract_chain.get_shared_llm')
    def test_create_extraction_chain_unsupported_type(self, mock_get_llm):
        """Test error for unsupported extraction type."""
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        with pytest.raises(ValueError, match="Unsupported document type"):
            create_extraction_chain("unknown")


class TestExtractionChainGetters:
    """Test singleton getter functions."""

    def setup_method(self):
        """Reset singleton instances before each test."""
        import app.chains.extract_chain
        app.chains.extract_chain._financial_chain_instance = None
        app.chains.extract_chain._contract_chain_instance = None

    @patch('app.chains.extract_chain.get_shared_llm')
    def test_get_financial_extraction_chain_singleton(self, mock_get_llm):
        """Test financial extraction chain singleton."""
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        chain1 = get_financial_extraction_chain()
        chain2 = get_financial_extraction_chain()

        assert chain1 is chain2  # Same instance

    @patch('app.chains.extract_chain.get_shared_llm')
    def test_get_contract_extraction_chain_singleton(self, mock_get_llm):
        """Test contract extraction chain singleton."""
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        chain1 = get_contract_extraction_chain()
        chain2 = get_contract_extraction_chain()

        assert chain1 is chain2  # Same instance

    @patch('app.chains.extract_chain.get_shared_llm')
    def test_get_extraction_chain_for_financial(self, mock_get_llm):
        """Test getting extraction chain for financial documents."""
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        chain_invoice = get_extraction_chain("invoice")
        chain_receipt = get_extraction_chain("receipt")

        assert chain_invoice is not None
        assert chain_receipt is not None
        # Both should use the same financial chain
        assert chain_invoice is chain_receipt

    @patch('app.chains.extract_chain.get_shared_llm')
    def test_get_extraction_chain_for_contract(self, mock_get_llm):
        """Test getting extraction chain for contracts."""
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        chain = get_extraction_chain("contract")
        assert chain is not None

    @patch('app.chains.extract_chain.get_shared_llm')
    def test_get_extraction_chain_unsupported(self, mock_get_llm):
        """Test error for unsupported document type."""
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        with pytest.raises(ValueError, match="Unsupported document type"):
            get_extraction_chain("unknown")


class TestExtractionFunctions:
    """Test extraction convenience functions."""

    def setup_method(self):
        """Reset singleton instances before each test."""
        import app.chains.extract_chain
        app.chains.extract_chain._financial_chain_instance = None
        app.chains.extract_chain._contract_chain_instance = None

    def test_extract_from_document_function_exists(self):
        """Test that extract_from_document function is callable."""
        assert callable(extract_from_document)

    @patch('app.chains.extract_chain.get_shared_llm')
    def test_extract_from_document_unsupported_type(self, mock_get_llm):
        """Test error when extracting from unsupported document type."""
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        with pytest.raises(ValueError, match="Unsupported document type"):
            extract_from_document("test", "unknown")


class TestExtractionOutputModels:
    """Test that output models are correctly structured."""

    def test_extracted_financial_model_fields(self):
        """Test ExtractedFinancial model has correct fields."""
        # Verify model can be instantiated with minimal data
        model = ExtractedFinancial()
        assert model.company is None
        assert model.date is None
        assert model.total_amount is None
        assert model.currency is None
        assert model.items is None
        assert model.invoice_number is None

    def test_extracted_contract_model_fields(self):
        """Test ExtractedContract model has correct fields."""
        # Verify model can be instantiated with minimal data
        model = ExtractedContract()
        assert model.parties is None
        assert model.effective_date is None
        assert model.expiration_date is None
        assert model.key_obligations is None
        assert model.contract_type is None

    def test_extracted_financial_with_field_values(self):
        """Test ExtractedFinancial with actual field values."""
        from app.models.output_models import FieldValue

        field_value = FieldValue(value="Test Corp", confidence=0.95)
        model = ExtractedFinancial(company=field_value)

        assert model.company.value == "Test Corp"
        assert model.company.confidence == 0.95

    def test_extracted_contract_with_parties(self):
        """Test ExtractedContract with parties."""
        from app.models.output_models import FieldValue

        party1 = FieldValue(value="Party A Inc.", confidence=0.98)
        party2 = FieldValue(value="Party B Corp.", confidence=0.96)
        model = ExtractedContract(parties=[party1, party2])

        assert len(model.parties) == 2
        assert model.parties[0].value == "Party A Inc."


class TestExtractionIntegration:
    """Integration tests for extraction chains."""

    @patch('app.chains.extract_chain.get_shared_llm')
    def test_financial_and_contract_chains_independent(self, mock_get_llm):
        """Test that financial and contract chains are independent."""
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        # Reset singletons
        import app.chains.extract_chain
        app.chains.extract_chain._financial_chain_instance = None
        app.chains.extract_chain._contract_chain_instance = None

        financial_chain = get_financial_extraction_chain()
        contract_chain = get_contract_extraction_chain()

        # Should be different instances
        assert financial_chain is not contract_chain

    @patch('app.chains.extract_chain.get_shared_llm')
    def test_extraction_chain_missing_api_key(self, mock_get_llm):
        """Test error handling when API key is missing."""
        mock_get_llm.side_effect = ValueError(
            "OPENAI_API_KEY environment variable is not set."
        )

        with pytest.raises(ValueError, match="Cannot create extraction chain"):
            create_financial_extraction_chain()

    def test_extraction_prompt_format_compatibility(self):
        """Test that extraction prompts are compatible with LCEL."""
        financial_prompt = get_extraction_prompt("invoice")
        contract_prompt = get_extraction_prompt("contract")

        # Both should be ChatPromptTemplate instances
        assert hasattr(financial_prompt, 'messages')
        assert len(financial_prompt.messages) == 2

        assert hasattr(contract_prompt, 'messages')
        assert len(contract_prompt.messages) == 2
