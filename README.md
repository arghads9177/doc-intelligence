# AI Document Intelligence System

An intelligent document processing pipeline that classifies, extracts, validates, and summarizes information from multiple document types using LangChain and OpenAI's GPT-4o.

## 🎯 Overview

This system processes documents through a sophisticated multi-stage pipeline:

1. **Ingestion**: Load documents from various sources (PDF, plain text)
2. **Classification**: Determine document type (invoice, receipt, contract, etc.)
3. **Extraction**: Extract structured data with confidence scores
4. **Validation**: Hybrid rule-based and AI-powered validation
5. **Summarization**: Generate concise document summaries
6. **Response**: Return unified, validated JSON responses

## 🏗️ Architecture

### Data Flow

```
Client Request
    ↓
┌─────────────────────────────────────────┐
│      FastAPI Endpoint                    │
│    (POST /api/analyze)                  │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│    Ingestion Service                     │
│  (TextLoader / PyPDFLoader)             │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│    Classification Chain (LCEL)           │
│  ChatPromptTemplate → ChatOpenAI         │
│  → JsonOutputParser                     │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│    Extraction Chain (LCEL)               │
│  Type-aware prompts (Financial/Contract)│
│  → ChatOpenAI → PydanticOutputParser    │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│    Validation Engine (Hybrid)            │
│  ├─ Rule Layer (Python)                 │
│  └─ AI Validation Chain (LCEL)          │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│    Summarization Chain (LCEL)            │
│  ChatPromptTemplate → ChatOpenAI         │
│  → StrOutputParser                      │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│    Response Builder                      │
│  (Unified JSON Assembly)                │
└────────────┬────────────────────────────┘
             ↓
        JSON to Client
```

### Project Structure

```
doc-intelligence/
│
├── app/
│   ├── main.py                      # FastAPI initialization & router setup
│   │
│   ├── routes/
│   │   └── analyze.py               # POST /api/analyze endpoint
│   │
│   ├── chains/                      # LangChain LCEL pipelines
│   │   ├── classify_chain.py        # Classification pipeline
│   │   ├── extract_chain.py         # Extraction pipeline
│   │   ├── validate_chain.py        # AI validation pipeline
│   │   └── summarize_chain.py       # Summarization pipeline
│   │
│   ├── services/
│   │   ├── ingestion.py             # Document ingestion (LangChain loaders)
│   │   ├── validator.py             # Rule-based + AI validation logic
│   │   └── response_builder.py      # Final response assembly
│   │
│   ├── models/
│   │   ├── request_models.py        # Pydantic request schemas
│   │   └── output_models.py         # Pydantic output schemas
│   │
│   ├── prompts/                     # LangChain prompt templates
│   │   ├── classify_prompt.py
│   │   ├── extract_prompt.py
│   │   ├── validate_prompt.py
│   │   └── summarize_prompt.py
│   │
│   └── utils/
│       ├── llm.py                   # Shared ChatOpenAI instance
│       └── confidence.py            # Confidence score utilities
│
├── tests/
│   ├── test_classify_chain.py
│   ├── test_extract_chain.py
│   ├── test_validator.py
│   └── test_api.py
│
├── sample_docs/                     # Sample .txt and .pdf files for testing
│
├── .env                             # Environment variables (OPENAI_API_KEY)
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Project metadata
├── main.py                          # Entry point (development)
└── README.md                        # This file
```

## 🔑 Key Components

### LangChain Integration

- **LCEL Pipelines**: Composable prompt → LLM → parser chains
- **ChatOpenAI**: Shared instance with temperature=0 for determinism
- **Pydantic Parsers**: `JsonOutputParser`, `PydanticOutputParser`, `StrOutputParser`
- **Document Loaders**: LangChain's `TextLoader` and `PyPDFLoader`

### Supported Document Types

- **Financial**: Invoices, Receipts
- **Contracts**: Legal agreements
- **Unknown**: Fallback for unrecognized types

### Extraction Schema

Each extracted document includes:
- Field value
- Confidence score (0-1)
- Source/notes

### Validation Strategy

**Rule Layer** (deterministic):
- Exact numeric comparison (amounts)
- Datetime parsing and comparison
- String matching with fuzzy ratio threshold

**AI Layer** (runs when rules flag issues):
- Context-aware reasoning
- Exception handling (e.g., name abbreviations)
- Enriched issue explanations

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
uv venv

# Activate
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
# Create .env file
echo "OPENAI_API_KEY=your-key-here" > .env
```

### 3. Run the API

```bash
python main.py
```

Server runs at: `http://localhost:8000`

### 4. API Endpoint

**POST** `/api/analyze`

**Request Body:**
```json
{
  "documents": [
    {
      "filename": "invoice.pdf",
      "content_type": "application/pdf",
      "file_bytes": "<base64-encoded>"
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "processed_documents": [
    {
      "filename": "invoice.pdf",
      "doc_type": "invoice",
      "extracted_fields": {
        "company": {
          "value": "Acme Inc.",
          "confidence": 0.98
        },
        "total_amount": {
          "value": 1500.00,
          "confidence": 0.95
        }
      },
      "validation_report": {...},
      "summary": "Invoice from Acme Inc. for $1500 dated 2024-03-15..."
    }
  ]
}
```

## 📋 Development Phases

| Phase | Scope | Est. Time | Status |
|-------|-------|-----------|--------|
| 1 | Project setup, models, shared LLM, .env | 0.5 day | 🔵 Pending |
| 2 | Ingestion service, classify chain | 0.5 day | ⚪ Not started |
| 3 | Extraction chain with branches | 1 day | ⚪ Not started |
| 4 | Hybrid validation engine | 1 day | ⚪ Not started |
| 5 | Summarizer, response builder, routes | 0.5 day | ⚪ Not started |
| 6 | Testing, docs, sample data, cleanup | 0.5 day | ⚪ Not started |

**Total Estimated Time**: ~4 days

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_classify_chain.py

# Run with verbose output
pytest -v

# Run with async support
pytest -v --asyncio-mode=auto
```

## 🔧 Technologies

- **LangChain 0.1.14** - LLM orchestration and chains
- **FastAPI 0.104.1** - Web framework
- **Pydantic 2.0+** - Data validation
- **OpenAI API** - GPT-4o language model
- **PDFPlumber 0.10.3** - PDF extraction
- **Pytest 7.4.3** - Testing framework

## 📝 Environment Variables

```env
# Required
OPENAI_API_KEY=sk-...

# Optional
LOG_LEVEL=INFO
API_PORT=8000
LLM_MODEL=gpt-4o
LLM_TEMPERATURE=0
```

## 🔐 Security Notes

- Store `OPENAI_API_KEY` securely (use `.env` locally, secrets in production)
- Validate all file uploads before processing
- Sanitize document content before sending to LLM
- Implement rate limiting for API endpoints

## 📖 Documentation

- **API Docs**: Auto-generated at `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🤝 Contributing

Follow these conventions:
- Use type hints for all functions
- Document complex logic with docstrings
- Write tests alongside new features
- Keep chains modular and reusable

## 📄 License

See LICENSE file for details.

---

**Status**: Phase 1 Ready 🚀
An AI-powered Document Intelligence System
