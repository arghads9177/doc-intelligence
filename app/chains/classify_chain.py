"""
Classification chain for document type classification.

LCEL pipeline that classifies documents into categories using LangChain.
Combines the classification prompt with the shared LLM and JSON output parser.
"""

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import Runnable

from app.prompts.classify_prompt import classify_prompt
from app.utils import get_shared_llm


def create_classify_chain() -> Runnable:
    """
    Create the document classification chain using LCEL.

    Returns:
        Runnable: LCEL chain that takes document_text and returns {"doc_type": "..."}

    Raises:
        ValueError: If OPENAI_API_KEY is not configured
    """
    try:
        llm = get_shared_llm()
    except ValueError as e:
        if "OPENAI_API_KEY" in str(e):
            raise ValueError(
                "Cannot create classification chain: OPENAI_API_KEY not configured. "
                "Please set the API key in .env file or environment variables."
            ) from e
        raise

    parser = JsonOutputParser()

    # LCEL pipeline: prompt | llm | parser
    chain = classify_prompt | llm | parser

    return chain


# Singleton instance - created once and reused on first call
_classify_chain_instance: Runnable | None = None


def get_classify_chain() -> Runnable:
    """
    Get the shared classification chain instance (singleton pattern).
    
    Returns:
        Runnable: The shared classification chain instance
    """
    global _classify_chain_instance
    if _classify_chain_instance is None:
        _classify_chain_instance = create_classify_chain()
    return _classify_chain_instance


# Lazy import - don't instantiate until needed
def __getattr__(name):
    if name == "classify_chain":
        return get_classify_chain()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def classify_document(document_text: str) -> dict:
    """
    Classify a document based on its text content.

    Args:
        document_text: The text content of the document to classify

    Returns:
        dict: Classification result with "doc_type" field
               Values: "invoice", "receipt", "contract", or "unknown"

    Example:
        >>> result = classify_document("Invoice #123 from ABC Corp for $500")
        >>> print(result)
        {"doc_type": "invoice"}
    """
    chain = get_classify_chain()
    result = chain.invoke({"document_text": document_text})
    return result


async def aclassify_document(document_text: str) -> dict:
    """
    Async version of classify_document.

    Args:
        document_text: The text content of the document to classify

    Returns:
        dict: Classification result with "doc_type" field
    """
    chain = get_classify_chain()
    result = await chain.ainvoke({"document_text": document_text})
    return result


# Export the chain and functions
__all__ = [
    "create_classify_chain",
    "get_classify_chain",
    "classify_document",
    "aclassify_document",
]
