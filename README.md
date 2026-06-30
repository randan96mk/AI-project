# AI Agent + RAG + MCP — Proof of Concept

A local AI system combining an autonomous agent, a retrieval-augmented generation (RAG) knowledge base, and a Model Context Protocol (MCP) HTTP server — all running locally with Ollama.

## Quick Start (5 steps)

```bash
# 1. Create virtual environment
python3 -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize RAG (loads docs into vector DB)
python rag.py

# 4a. Terminal 1 — start MCP server
python mcp_server.py

# 4b. Terminal 2 — start agent (interactive)
python agent.py

# 4c. Terminal 3 — run tests
python mcp_client.py
```

## What It Does

| Component | File | Role |
|-----------|------|------|
| **Agent** | `agent.py` | ReAct loop: thinks, picks tool, observes, repeats |
| **RAG** | `rag.py` | Embeds docs locally, searches by similarity |
| **MCP Server** | `mcp_server.py` | FastAPI HTTP server exposing tools as REST API |
| **Test Client** | `mcp_client.py` | Automated test suite for the MCP server |

## Architecture

```
User Input
    │
    ▼
Agent (ReAct loop, Ollama gemma4:e4b)
    │
    ├──► calculator       — math expressions
    ├──► read_file        — read file contents
    ├──► write_file       — write to file
    ├──► get_time         — current datetime
    └──► search_rag       — vector DB search
                │
                ▼
         Chroma Vector DB
         (HuggingFace embeddings)

MCP Server (FastAPI :8000)
    ├── GET  /health
    ├── GET  /tools
    ├── POST /call    ← single tool
    └── POST /batch   ← multiple tools
```

## Example Usage

**Agent (natural language):**
```
You: Calculate 15% of 2500
Agent: 375.0

You: What is the NIFTY long straddle strategy?
Agent: [searches RAG, returns strategy from trading.md]
```

**MCP API (curl):**
```bash
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"calculator","arguments":{"expression":"2+2"}}'
# → {"tool_name":"calculator","result":"4","success":true}
```

## Prerequisites

- Python 3.9+
- Ollama running with `gemma4:e4b` model: `ollama pull gemma4:e4b`

See `QUICK_START.md` for detailed setup and troubleshooting.
