# 🤖 RAG Chatbot

A Retrieval-Augmented Generation chatbot that answers questions from your documents using LangChain, OpenAI, and ChromaDB.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![LangChain](https://img.shields.io/badge/LangChain-0.3-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39-red)

## Features

- **Document Ingestion** - Upload PDF, TXT, and Markdown files
- **Smart Chunking** - Recursive text splitting with configurable size/overlap
- **Vector Search** - ChromaDB for fast similarity search
- **RAG Pipeline** - Context-aware answers with source citations
- **Chat History** - Multi-turn conversations with memory
- **Clean UI** - Streamlit chat interface with source previews
- **REST API** - FastAPI backend for programmatic access
- **Docker Ready** - Containerized deployment

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Streamlit UI  │────▶│   FastAPI API    │────▶│   Retriever     │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                          ┌───────────────┼───────────────┐
                                          ▼               ▼               ▼
                                   ┌────────────┐  ┌────────────┐  ┌────────────┐
                                   │ VectorDB   │  │   LLM      │  │  Ingest    │
                                   │ (ChromaDB) │  │ (OpenAI)   │  │ (LangChain)│
                                   └────────────┘  └────────────┘  └────────────┘
```

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/rag-chatbot.git
cd rag-chatbot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Run the Application

**Start the backend:**
```bash
uvicorn app.main:app --reload --port 8000
```

**Start the frontend (new terminal):**
```bash
streamlit frontend/app.py
```

Open http://localhost:8501 in your browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/upload` | Upload and process a document |
| `POST` | `/chat` | Send a query and get an answer |
| `GET` | `/stats` | Get collection statistics |
| `DELETE` | `/collection` | Delete the vector collection |

### Example API Usage

```bash
# Upload a document
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf"

# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is this document about?"}'
```

## Docker Deployment

```bash
docker build -t rag-chatbot .
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-your-key rag-chatbot
```

## Configuration

All settings can be configured via environment variables or `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | - | Your OpenAI API key |
| `LLM_MODEL` | `gpt-4o-mini` | Model to use |
| `CHUNK_SIZE` | `1000` | Text chunk size |
| `CHUNK_OVERLAP` | `200` | Chunk overlap |
| `TOP_K` | `4` | Number of results to retrieve |

## Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **AI/ML**: LangChain, OpenAI, ChromaDB
- **Frontend**: Streamlit
- **Containerization**: Docker

## License

MIT
