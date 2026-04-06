"""
Shared LLM configuration and instance.

Provides a centralized ChatOpenAI instance used across all chains.
This ensures consistent configuration and single point of LLM management.
"""

import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


def get_llm() -> ChatOpenAI:
    """
    Create and return a configured ChatOpenAI instance.
    
    Uses environment variables for configuration:
    - OPENAI_API_KEY: OpenAI API key
    - LLM_MODEL: Model name (default: gpt-4o)
    - LLM_TEMPERATURE: Temperature for randomness (default: 0)
    - LLM_MAX_TOKENS: Max tokens per response (default: 4000)
    - LLM_REQUEST_TIMEOUT: Request timeout in seconds (default: 60)
    - LLM_MAX_RETRIES: Max retry attempts (default: 3)
    
    Returns:
        ChatOpenAI: Configured language model instance
    
    Raises:
        ValueError: If OPENAI_API_KEY is not set
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is not set. "
            "Please configure it in .env file or system environment."
        )
    
    model_name = os.getenv("LLM_MODEL", "gpt-4o")
    temperature = float(os.getenv("LLM_TEMPERATURE", "0"))
    max_tokens = int(os.getenv("LLM_MAX_TOKENS", "4000"))
    request_timeout = int(os.getenv("LLM_REQUEST_TIMEOUT", "60"))
    max_retries = int(os.getenv("LLM_MAX_RETRIES", "3"))
    
    llm = ChatOpenAI(
        api_key=api_key,
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        request_timeout=request_timeout,
        max_retries=max_retries,
    )
    
    return llm


# Singleton instance - created once and reused on first call
_llm_instance: ChatOpenAI | None = None


def get_shared_llm() -> ChatOpenAI:
    """
    Get the shared LLM instance (singleton pattern).
    
    Lazily creates the LLM instance on first call.
    
    Returns:
        ChatOpenAI: The shared language model instance
    """
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = get_llm()
    return _llm_instance


# Lazy import - don't instantiate until needed
def __getattr__(name):
    if name == "llm":
        return get_shared_llm()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
