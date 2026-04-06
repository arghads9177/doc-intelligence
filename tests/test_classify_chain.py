"""
Tests for the document classification chain.

Note: Tests that actually execute the LCEL chain with LLM require OPENAI_API_KEY.
This file includes tests that can run without a real API key, and serves as an
example structure for more comprehensive testing once the API key is available.
"""

import pytest
from unittest.mock import patch, MagicMock

from app.chains.classify_chain import create_classify_chain, get_classify_chain, classify_document
from app.prompts.classify_prompt import classify_prompt


class TestClassifyChain:
    """Test cases for the classification chain."""

    def setup_method(self):
        """Set up test fixtures before each test."""
        # Reset the singleton chain instance for each test
        import app.chains.classify_chain
        app.chains.classify_chain._classify_chain_instance = None

    @patch('app.chains.classify_chain.get_shared_llm')
    def test_create_classify_chain(self, mock_get_llm):
        """Test that create_classify_chain returns a Runnable."""
        # Mock the LLM
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        chain = create_classify_chain()
        assert chain is not None
        # Check that it's an LCEL chain (has pipe operations)
        assert hasattr(chain, 'invoke')

        # Verify LLM was retrieved
        mock_get_llm.assert_called_once()

    @patch('app.chains.classify_chain.get_shared_llm')
    def test_classify_chain_structure(self, mock_get_llm):
        """Test that the global classify_chain getter works."""
        # Mock the LLM
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        chain = get_classify_chain()
        assert chain is not None
        # Check that it's an LCEL chain (has pipe operations)
        assert hasattr(chain, 'invoke')

    def test_classify_document_function_exists(self):
        """Test that classify_document function is callable."""
        # Just verify the function exists and is callable
        assert callable(classify_document)


class TestClassifyPrompt:
    """Test cases for the classification prompt template."""

    def test_prompt_structure(self):
        """Test that the prompt template has correct structure."""
        assert classify_prompt is not None
        assert len(classify_prompt.messages) == 2  # system + human

    def test_prompt_messages(self):
        """Test that prompt messages contain expected content."""
        messages = classify_prompt.messages

        # Check system message
        system_msg = messages[0]
        assert "expert document classifier" in str(system_msg).lower()
        assert "invoice" in str(system_msg)
        assert "receipt" in str(system_msg)
        assert "contract" in str(system_msg)
        assert "unknown" in str(system_msg)

        # Check human message
        human_msg = messages[1]
        assert "{document_text}" in str(human_msg)
        assert "JSON object" in str(human_msg)
