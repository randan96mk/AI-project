# Quick Start Guide

## Prerequisites

- macOS / Linux with Python 3.9+
- [Ollama](https://ollama.ai) installed and running
- `gemma4:e4b` model pulled: `ollama pull gemma4:e4b`

## 1. Verify Ollama

```bash
curl http://localhost:11434/api/tags
# Should return JSON with models list
```

If Ollama is not running:
```bash
# macOS
open /Applications/Ollama.app
# or
/Applications/Ollama.app/Contents/MacOS/Ollama serve
```

## 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate       # macOS/Linux
# venv\Scripts\activate        # Windows
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Initialize RAG System

```bash
python rag.py
# Loads data/docs/*.md into Chroma vector DB
# Expected: "RAG initialized successfully."
```

## 5. Run Components (3 terminals)

**Terminal 1 — MCP Server:**
```bash
source venv/bin/activate
python mcp_server.py
# Expected: INFO: Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 — Agent:**
```bash
source venv/bin/activate
python agent.py
# Shows 3 example tasks, then interactive prompt:
# You: (type anything)
```

**Terminal 3 — Test Client:**
```bash
source venv/bin/activate
python mcp_client.py
# Expected: ✓ All 7 tests passed
```

## 6. Verify with curl

```bash
# Health check
curl http://localhost:8000/health

# List tools
curl http://localhost:8000/tools

# Test calculator
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"calculator","arguments":{"expression":"2+2"}}'

# Test batch
curl -X POST http://localhost:8000/batch \
  -H "Content-Type: application/json" \
  -d '[{"tool_name":"calculator","arguments":{"expression":"50+50"}},{"tool_name":"get_time","arguments":{}}]'
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Activate venv: `source venv/bin/activate` |
| `Connection refused :8000` | Start server: `python mcp_server.py` |
| `Connection refused :11434` | Start Ollama app |
| `gemma4:e4b not found` | `ollama pull gemma4:e4b` |
| Chroma DB issues | `rm -rf data/chroma_db && python rag.py` |
| Agent is slow | Lower `max_iterations=3` in `agent.py` |

## Add Your Own Knowledge

```bash
# Drop any .md file into data/docs/
cp my-notes.md data/docs/

# Re-initialize RAG
rm -rf data/chroma_db
python rag.py
```
