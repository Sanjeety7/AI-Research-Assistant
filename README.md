<div align="center">

<img src="https://img.shields.io/badge/AI_Research_Assistant-v1.0-7c3aed?style=for-the-badge&logo=sparkles&logoColor=white" />

# 🔬 AI Research Assistant

### A full-stack intelligent research platform powered by RAG, multi-model routing & real-time web search

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![OpenAI](https://img.shields.io/badge/GPT--4o-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com)
[![Pinecone](https://img.shields.io/badge/Pinecone-VectorDB-00C8B4?style=flat-square)](https://pinecone.io)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C?style=flat-square)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

> Upload PDFs → Ask questions → Get grounded, source-cited answers from the world's best AI models.

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [RAG Pipeline](#-rag-pipeline-deep-dive)
- [Installation](#-installation--setup)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)

---

## 🎯 Overview

The **AI Research Assistant** is a production-grade full-stack application combining:

- 📄 **PDF Document Intelligence** — upload & semantically index your own documents
- 🧠 **RAG (Retrieval-Augmented Generation)** — grounded answers from your knowledge base
- 🌐 **Live Web Search** — real-time context from the internet
- 🤖 **Multi-Model Routing** — intelligently picks GPT-4o, Claude 3.5 Sonnet, or Gemini 1.5 Pro

Built entirely from scratch with **Python (FastAPI)** backend and **vanilla HTML/CSS/JS** frontend — demonstrating end-to-end AI application development from vector indexing to response delivery.

| Metric | Value |
|--------|-------|
| AI Models Integrated | 3 (GPT-4o, Claude 3.5, Gemini 1.5 Pro) |
| PDF Upload Limit | 200 MB |
| Avg. Response Time | ~2.5 seconds |
| Context Routing Modes | RAG / Web Search / RAG + Web |

---

## 🖥️ Live Demo

### Welcome Screen
The assistant greets you with smart research prompt suggestions and an intuitive sidebar for document management.

![Welcome Screen](screenshots/screen_06.png)

---

### Document Analysis — RAG in Action
After uploading a PDF, ask any question. The system retrieves relevant chunks from Pinecone and generates a grounded answer with a **HIGH confidence rating**.

![RAG Response](screenshots/screen_01.png)

---

### Source Cards — Full Transparency
Every response surfaces the exact document chunks that were used, complete with **similarity scores** (0.74–0.75).

![Source Cards](screenshots/screen_03.png)

---

### Session Statistics
Live tracking of token usage and estimated API cost per session.

![Session Stats](screenshots/screen_05.png)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 PDF Intelligence | Upload PDFs up to 200MB — auto-extracted, chunked & indexed into Pinecone |
| 🔍 RAG + Web Hybrid | Combine private knowledge base with live web search |
| 🤖 Multi-Model Routing | Auto-selects the best model based on query type |
| 📊 Source Transparency | Every response shows retrieved chunks + similarity scores |
| 📈 Session Stats | Real-time token tracking + estimated API cost |
| 🎯 Confidence Scoring | HIGH / MEDIUM / LOW confidence rating + response latency |
| 📝 Document Summarization | One-click summary of any uploaded PDF |
| 💾 Export Chat | Download full conversation history |
| 🌙 Dark Mode UI | Polished dark-first interface — no framework dependencies |

---

## 🏗️ System Architecture

```
┌─────────┐     HTTP/JSON     ┌──────────────────┐
│  User   │ ──────────────▶  │  FastAPI Backend  │
│ Browser │ ◀──────────────  │   (Python)        │
└─────────┘                  └────────┬─────────┘
                                      │
               ┌──────────────────────┼────────────────────┐
               ▼                      ▼                     ▼
        ┌─────────────┐      ┌───────────────┐    ┌──────────────┐
        │  Pinecone   │      │   LLM APIs    │    │  Web Search  │
        │ Vector DB   │      │ ┌───────────┐ │    │  (Live ctx)  │
        │ Semantic    │      │ │  GPT-4o   │ │    └──────────────┘
        │ Search      │      │ ├───────────┤ │
        └─────────────┘      │ │  Claude   │ │
                             │ ├───────────┤ │
        ┌─────────────┐      │ │  Gemini   │ │
        │  Embeddings │      │ └───────────┘ │
        │ text-emb-3  │      └───────────────┘
        │   -small    │
        └─────────────┘
               ▲
        ┌─────────────┐
        │  PDF Input  │
        │  PyMuPDF    │
        └─────────────┘
```

### RAG Query Flow

```
User Query
    │
    ▼
[1] Generate query embedding (text-embedding-3-small)
    │
    ▼
[2] Semantic search in Pinecone → Top-K chunks retrieved
    │
    ▼
[3] (Optional) Live web search results merged
    │
    ▼
[4] Context + query sent to selected LLM
    │
    ▼
[5] Grounded response returned with source citations
    │
    ▼
UI displays answer + source cards + confidence + token stats
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | Python web framework — REST API |
| **Uvicorn** | ASGI server |
| **LangChain** | RAG orchestration |
| **PyMuPDF (fitz)** | PDF text extraction |
| **Pydantic** | Request/response data validation |
| **python-dotenv** | Environment config management |

### AI & Vector
| Service | Model | Purpose |
|---------|-------|---------|
| **OpenAI** | gpt-4o | Primary LLM — general purpose |
| **OpenAI** | text-embedding-3-small | Query & document embeddings |
| **Anthropic** | claude-3-5-sonnet-20241022 | Code-heavy queries |
| **Google AI** | gemini-1.5-pro | Large context window tasks |
| **Pinecone** | Serverless index | Vector storage & semantic search |

### Frontend
| Technology | Purpose |
|------------|---------|
| **HTML5 / CSS3** | Structure & dark-mode styling |
| **Vanilla JavaScript** | Chat logic, API calls, UI state |

---

## 🧠 RAG Pipeline Deep-Dive

### Document Ingestion

```python
def ingest_pdf(file_path: str):
    # Step 1: Extract text using PyMuPDF
    doc = fitz.open(file_path)
    full_text = " ".join([page.get_text() for page in doc])

    # Step 2: Chunk into ~500 token segments with overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50
    )
    chunks = text_splitter.split_text(full_text)

    # Step 3: Generate embeddings via OpenAI
    embeddings = openai.embeddings.create(
        model="text-embedding-3-small",
        input=chunks
    )

    # Step 4: Upsert vectors to Pinecone
    index.upsert(vectors=list(zip(ids, embeddings, metadata)))
```

### Context Routing Modes

| Mode | Description | Best For |
|------|-------------|----------|
| `RAG Only` | Searches uploaded document knowledge base only | Private document Q&A |
| `Web Search Only` | Live internet search for current info | News, real-time data |
| `RAG + Web Search` | Combines both sources (default) | Comprehensive research |

### Model Auto-Routing Logic

```python
if mode == "auto-route":
    if is_code_query(query):
        model = "claude-3-5-sonnet"    # Best at coding & reasoning
    elif needs_large_context(query):
        model = "gemini-1.5-pro"       # 2M token context window
    else:
        model = "gpt-4o"               # General purpose flagship
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.10+
- API keys: OpenAI, Pinecone (required) · Anthropic, Google AI (optional)

### Step 1 — Clone the repository

```bash
git clone https://github.com/yourusername/ai-research-assistant.git
cd ai-research-assistant
```

### Step 2 — Navigate to backend & install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 3 — Configure environment variables

Create `backend/.env`:

```env
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=AIzaSy...
PINECONE_API_KEY=pcsk-...
PINECONE_INDEX_NAME=research-assistant
```

### Step 4 — Start the backend server

```bash
python -m uvicorn app.main:app --reload
```

Server runs at `http://localhost:8000`

### Step 5 — Open the frontend

Open `frontend/index.html` in your browser.

---

## 📖 Usage

| Action | How | Notes |
|--------|-----|-------|
| Upload a PDF | Click **Upload** in sidebar | Max 200MB, auto-indexed |
| Ask a question | Type in chat input → Enter | Uses selected model + routing |
| Summarize document | Click **Summarize Document** | Full RAG pipeline runs |
| Switch AI model | **Model Selection** dropdown | GPT-4o / Claude / Gemini / Auto |
| Change context mode | **Context Routing** dropdown | RAG / Web / RAG + Web |
| View sources | Scroll below any response | Similarity scores shown |
| Export session | Click **Export** in sidebar | Downloads chat as file |

---

## 📁 Project Structure

```
ai_research_assistant/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app, all API endpoints
│   │   ├── rag.py           # RAG pipeline — retrieval + generation
│   │   ├── models.py        # Pydantic request/response schemas
│   │   └── utils.py         # PDF extraction + chunking helpers
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # API keys (not committed to git)
└── frontend/
    ├── index.html           # Single-page application
    ├── style.css            # Dark-mode styling
    └── app.js               # Chat logic, REST calls, UI state
```

---

## 🔌 API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/query` | POST | Submit a research question |
| `/upload-pdf` | POST | Upload and index a PDF document |
| `/summarize` | POST | Summarize the uploaded document |
| `/health` | GET | Backend health check |

### Example Request

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key findings?",
    "model": "auto-route",
    "context_mode": "rag_and_web"
  }'
```

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built with ❤️ by **Sanjet Kumar** · Internship Assignment Submission 2026

*FastAPI · LangChain · Pinecone · OpenAI · Anthropic · Google Gemini*

</div>
