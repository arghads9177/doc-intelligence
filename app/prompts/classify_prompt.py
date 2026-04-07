"""
Classification prompt template for document type classification.

Uses ChatPromptTemplate to create structured prompts for classifying
documents into categories: invoice, receipt, contract, or unknown.
"""

from langchain_core.prompts import ChatPromptTemplate

# System message for document classification
CLASSIFY_SYSTEM_PROMPT = """
You are an expert document classifier specializing in financial and legal documents.

Your task is to analyze the provided document text and classify it into one of the following categories:

1. **invoice** - A bill or invoice requesting payment for goods or services, typically containing:
   - Company/vendor information
   - Itemized charges or services
   - Total amount due
   - Payment terms or due dates
   - Invoice number

2. **receipt** - A confirmation of payment received, typically containing:
   - Proof of payment
   - Transaction details
   - Amount paid
   - Date of transaction
   - Payment method

3. **contract** - A legal agreement between parties, typically containing:
   - Parties involved
   - Terms and conditions
   - Obligations and responsibilities
   - Effective dates
   - Signatures or legal language

4. **unknown** - Any document that doesn't clearly fit the above categories or contains insufficient information for classification.

IMPORTANT:
- Be precise and conservative in your classification
- If the document is ambiguous or doesn't contain enough information, classify as "unknown"
- Focus on the primary purpose and content of the document
- Return ONLY a JSON object with the "doc_type" field
"""

# Human message template
CLASSIFY_HUMAN_PROMPT = """
Please classify the following document:

Document Text:
{document_text}

Respond with a JSON object containing:
- "doc_type": one of "invoice", "receipt", "contract", or "unknown"
- "confidence": your confidence score from 0.0 to 1.0
"""

# Create the chat prompt template
classify_prompt = ChatPromptTemplate.from_messages([
    ("system", CLASSIFY_SYSTEM_PROMPT),
    ("human", CLASSIFY_HUMAN_PROMPT)
])

# Export the prompt for use in chains
__all__ = ["classify_prompt", "CLASSIFY_SYSTEM_PROMPT", "CLASSIFY_HUMAN_PROMPT"]
