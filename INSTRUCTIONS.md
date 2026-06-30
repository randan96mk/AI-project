# Agent + RAG + MCP POC - Complete Build Guide

**Version:** 1.0  
**Date:** January 2025  
**Status:** Ready for Claude Code Generation

---

## 📖 TABLE OF CONTENTS

1. [Project Overview](#project-overview)
2. [Quick Start (30 mins)](#quick-start-30-mins)
3. [Claude Code Generation Instructions](#claude-code-generation-instructions)
4. [Manual Setup (Alternative)](#manual-setup-alternative)
5. [Component Architecture](#component-architecture)
6. [API Documentation](#api-documentation)
7. [Verification Checklist](#verification-checklist)
8. [Troubleshooting](#troubleshooting)

---

## PROJECT OVERVIEW

### What You're Building

An AI system combining three components:

1. **Agent** - Autonomous reasoning with tool execution (REACT pattern)
2. **RAG** - Retrieval-Augmented Generation (document search)
3. **MCP** - Model Context Protocol (HTTP API server)

All three work together locally on your Mac mini with Ollama (gemma4:e4b).

### Tech Stack

```
LLM:           Ollama (gemma4:e4b) - Local, no API keys
Framework:     LangChain + FastAPI
Vector DB:     Chroma (persistent storage)
Embeddings:    HuggingFace (all-MiniLM-L6-v2)
Language:      Python 3.9+
```

### What You Get

- ~1000 lines of working Python code
- 4 core files (agent, rag, mcp_server, mcp_client)
- 8 git commits with clear progression
- Sample documentation and tests
- Ready to run immediately after setup

---

## QUICK START (30 MINS)

### Prerequisites

- macOS (Apple Silicon or Intel)
- Ollama running with `gemma4:e4b` model installed
- Python 3.9+ installed

### Step 1: Verify Ollama

```bash
# Check Ollama is listening
curl http://localhost:11434/api/tags

# Should return JSON with gemma4:e4b in models list
# If not, start Ollama:
/Applications/Ollama.app/Contents/MacOS/Ollama serve
# or simply: open /Applications/Ollama.app
```

### Step 2: Use Claude Code (Easiest)

**Option A: claude.ai web interface**
```
1. Go to https://claude.ai
2. Start new chat
3. Copy the entire "CLAUDE CODE GENERATION PROMPT" section below
4. Paste into chat
5. Click "Create Project" when Claude offers
6. Download the generated ZIP file
```

**Option B: Claude Desktop App**
```
1. Open Claude Desktop app
2. Click "Claude Code" tab
3. Click "+ New Project"
4. Paste the prompt below
5. Wait for generation
6. Download and extract
```

### Step 3: Setup Generated Project

```bash
# Navigate to extracted project
cd poc-repo

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize RAG system
python rag.py
```

### Step 4: Run in 3 Terminals

**Terminal 1 - MCP Server:**
```bash
source venv/bin/activate
python mcp_server.py

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# Keep this terminal running
```

**Terminal 2 - Agent (new terminal):**
```bash
source venv/bin/activate
python agent.py

# Shows example tasks, then interactive prompt:
# You: (type anything)
# Agent: (thinks and responds using tools)
```

**Terminal 3 - Test MCP (new terminal):**
```bash
source venv/bin/activate
python mcp_client.py

# Runs all tests automatically
# Shows: ✓ All tests passed
```

### Step 5: Verify It Works

```bash
# Test MCP API
curl http://localhost:8000/health
# Should return: {"status":"ok","service":"MCP Server"}

# Test calculator tool
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"calculator","arguments":{"expression":"2+2"}}'
# Should return: {"tool_name":"calculator","result":"4","success":true}
```

**✓ Done! System is working.**

---

## CLAUDE CODE GENERATION INSTRUCTIONS

### How to Generate the Project

**Step 1: Copy This Entire Section**

Copy everything from "CLAUDE CODE PROMPT START" to "CLAUDE CODE PROMPT END" below.

**Step 2: Paste into Claude Code**

- Go to https://claude.ai or Claude Desktop App
- Start a new chat or new project
- Paste the entire prompt
- Submit

**Step 3: Wait for Generation**

Claude will:
- Generate all 4 Python files
- Create folder structure
- Add sample documents
- Initialize git repository
- Make 8 commits
- Output setup instructions

**Step 4: Download & Extract**

Download the ZIP file → Extract to your machine

**Step 5: Follow Setup Section Above**

---

### CLAUDE CODE PROMPT START

```
You are a Python expert. Your task is to generate a simple, working POC 
(proof-of-concept) for an AI system combining:
1. An autonomous agent with tool execution
2. A Retrieval-Augmented Generation (RAG) system
3. A Model Context Protocol (MCP) server with HTTP API

The generated code must be:
- Complete: No stubs, all functions fully implemented
- Working: Runs immediately after setup with zero modifications
- Simple: POC-focused, ~1000 lines total, easy to understand
- Local-first: Uses Ollama (gemma4:e4b) locally, no API keys needed
- Documented: Clear comments, docstrings, and setup instructions

TECHNOLOGY STACK:
- LLM: Ollama (gemma4:e4b) via http://localhost:11434
- Framework: LangChain 0.1.11
- Vector DB: Chroma 0.4.24
- Embeddings: HuggingFace (all-MiniLM-L6-v2)
- HTTP Server: FastAPI 0.104.1 on port 8000
- Language: Python 3.9+

PROJECT STRUCTURE:
```
poc-repo/
├── agent.py              # Main agent with tools
├── rag.py                # RAG system (vector DB)
├── mcp_server.py         # HTTP API server
├── mcp_client.py         # Test client
├── requirements.txt      # Python dependencies
├── README.md             # Project overview
├── QUICK_START.md        # Setup instructions
├── .gitignore            # Git ignore rules
└── data/
    ├── docs/             # Knowledge base (sample docs)
    │   ├── trading.md
    │   └── workfront.md
    └── chroma_db/        # Vector DB (auto-created)
```

COMPONENT 1: AGENT (agent.py) - ~300 lines

The agent uses LangChain's ReAct pattern:
1. Reads a task
2. Thinks about what tools are needed
3. Executes the appropriate tool
4. Observes the result
5. Repeats until task is complete

Required Tools (implement all 5):
- calculator(expression): Evaluate math expressions
- read_file(path): Read file contents (first 1000 chars)
- write_file(path, content): Write to file
- get_time(): Return current date/time
- search_rag(query): Search knowledge base

Features:
- Use Ollama (gemma4:e4b) via LangChain
- REACT pattern with max 5 iterations
- Verbose logging of reasoning steps
- Interactive mode for testing
- Show 3 example tasks before interactive mode

COMPONENT 2: RAG (rag.py) - ~200 lines

The RAG system:
1. Loads markdown files from data/docs/
2. Chunks text (500 chars, 50 overlap)
3. Embeds using HuggingFace locally
4. Stores in Chroma vector DB
5. Searches by similarity (top-3 results)

Class: RAGSystem
- __init__(persist_dir): Initialize
- load_documents(docs_path): Load .md files
- search(query, k=3): Search with top-k results

Features:
- Persistent Chroma database
- Local embeddings (no API calls)
- Auto-create data/docs/ if missing
- Return chunk content + source + score

COMPONENT 3: MCP SERVER (mcp_server.py) - ~250 lines

FastAPI server exposing tools via HTTP API:

Endpoints:
- GET /health → {"status":"ok"}
- GET /tools → List all tools
- POST /call → Execute single tool
- POST /batch → Execute multiple tools

Request models:
```
ToolCall: tool_name, arguments
ToolResult: tool_name, result, success
```

Features:
- Port 8000
- All tools from agent.py exposed
- Error handling with HTTP codes
- Logging of all calls
- Support for batch execution

COMPONENT 4: TEST CLIENT (mcp_client.py) - ~150 lines

Python client to test MCP server:
- Health check
- List available tools
- Test each tool individually
- Test batch execution
- Show results

SAMPLE DATA (data/docs/)

Create 2 sample markdown files:

trading.md:
- NIFTY 50 options strategies
- Bitcoin long straddle setup
- Risk management guidelines
- Entry/exit timing

workfront.md:
- Workfront Fusion automation basics
- Marketo integration patterns
- Campaign setup steps
- Common issues and solutions

REQUIREMENTS.txt

```
langchain==0.1.11
langchain-community==0.0.36
ollama==0.1.34
chromadb==0.4.24
sentence-transformers==2.2.2
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
requests==2.31.0
```

DOCUMENTATION

README.md:
- 1-sentence project description
- Quick start (5 steps)
- What it does
- Architecture diagram (ASCII art)
- Example usage

QUICK_START.md:
- Prerequisites
- Virtual environment setup
- Dependency installation
- Ollama verification
- Running each component (3 terminals)
- Testing procedures

GIT COMMITS (in this order)

```
1. init: project structure
   - Add all directories
   - Add .gitignore, requirements.txt

2. feat: implement agent with tools
   - agent.py with 5 tools
   - Ollama integration
   - REACT pattern

3. feat: implement RAG system
   - rag.py with document loading
   - Chroma vector DB
   - Similarity search

4. feat: implement MCP server
   - mcp_server.py with all endpoints
   - Tool execution handlers
   - Error handling

5. feat: implement MCP client
   - mcp_client.py with tests
   - All tests passing

6. feat: add sample data
   - data/docs/ with markdown files
   - Sample initialization

7. docs: add README and QUICK_START
   - Complete setup guide
   - Usage examples
   - Troubleshooting

8. test: add example tests
   - Test scripts
   - Verification procedures
```

CODE QUALITY REQUIREMENTS

- All imports must be valid (tested)
- All functions have complete implementations (no stubs)
- All functions have docstrings with Args, Returns, Raises
- All code has type hints (where applicable)
- All code handles exceptions properly
- Async functions work correctly
- Setup takes 5 minutes from extracted zip
- All example scripts run without modification
- No hardcoded secrets or API keys
- No external API dependencies (all local)
- Git history is clean with 8 commits

EXPECTED FINAL OUTPUT

After generation, these commands should work:

```bash
# Setup (5 minutes)
cd poc-repo
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python rag.py

# Terminal 1: MCP Server
python mcp_server.py
# Output: "INFO:     Uvicorn running on http://0.0.0.0:8000"

# Terminal 2: Agent
python agent.py
# Shows 3 example tasks, then interactive mode

# Terminal 3: Test Client
python mcp_client.py
# Output: "✓ All tests passed"

# Terminal 4: Verify with curl
curl http://localhost:8000/health
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"calculator","arguments":{"expression":"2+2"}}'
```

GENERATE NOW

You have all requirements. Create:
1. All 4 main Python files (complete implementations)
2. Sample documentation (trading.md, workfront.md)
3. requirements.txt
4. README.md, QUICK_START.md, .gitignore
5. Git repository with 8 commits
6. data/docs/ and data/.gitkeep folders

The goal is a complete, working POC that demonstrates Agent + RAG + MCP 
in ~1000 lines of clean Python code, ready to run immediately.

Begin now.
```

### CLAUDE CODE PROMPT END

---

## MANUAL SETUP (ALTERNATIVE)

If Claude Code generation doesn't work or you prefer manual setup:

### Step 1: Copy Working Code Files

The three working Python files are already provided:
- `agent.py` - Copy to your project
- `mcp_server.py` - Copy to your project
- `mcp_client.py` - Copy to your project

### Step 2: Create requirements.txt

```bash
cat > requirements.txt << 'EOF'
langchain==0.1.11
langchain-community==0.0.36
ollama==0.1.34
chromadb==0.4.24
sentence-transformers==2.2.2
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
requests==2.31.0
EOF
```

### Step 3: Create Sample RAG File

```bash
mkdir -p data/docs

cat > data/docs/trading.md << 'EOF'
# Trading Strategies

## NIFTY 50 Options

### Long Straddle
- Entry: At-the-money (ATM) strikes
- Buy both Call and Put
- Profit from large price movements

### Short Straddle
- Sell ATM Call and Put
- Collect premium
- Risk: Unlimited if price moves sharply

## Risk Management
- Never risk more than 2% per trade
- Set stop loss at 1.5x entry premium
EOF
```

### Step 4: Setup Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python rag.py  # Initialize RAG
```

### Step 5: Run Components

```bash
# Terminal 1
python mcp_server.py

# Terminal 2
python agent.py

# Terminal 3
python mcp_client.py
```

---

## COMPONENT ARCHITECTURE

### Data Flow

```
User Input
    ↓
Agent (Thinks + Plans)
    ↓
Chooses Tool:
    ├→ Calculator
    ├→ File I/O
    ├→ RAG Search (vector DB)
    ├→ Get Time
    └→ Python Executor
    ↓
Tool Executes
    ↓
Agent Observes Result
    ↓
Agent Generates Response
    ↓
Output to User
```

### API Server Architecture

```
MCP Server (FastAPI, port 8000)
    ├── /health (GET)
    ├── /tools (GET) → List available tools
    ├── /call (POST) → Execute single tool
    └── /batch (POST) → Execute multiple tools
         ↓
    Tool Registry
         ↓
    Tool Execution
         ↓
    Response (JSON)
```

### RAG System

```
Data Flow:
markdown files → chunks → embeddings → vector DB → search → results

Technology:
- Loader: DirectoryLoader
- Chunker: RecursiveCharacterTextSplitter
- Embeddings: HuggingFaceEmbeddings
- DB: Chroma (persistent on disk)
- Search: Similarity search with scores
```

---

## API DOCUMENTATION

### Tool Endpoints

#### GET /health
Check if server is running
```bash
curl http://localhost:8000/health

Response:
{"status": "ok", "service": "MCP Server"}
```

#### GET /tools
List all available tools
```bash
curl http://localhost:8000/tools

Response:
{
  "tools": [
    {"name": "calculator", "description": "Evaluate math expressions"},
    {"name": "read_file", "description": "Read file contents"},
    ...
  ]
}
```

#### POST /call
Execute a single tool
```bash
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "calculator",
    "arguments": {"expression": "100 * 0.02"}
  }'

Response:
{
  "tool_name": "calculator",
  "result": "2.0",
  "success": true
}
```

#### POST /batch
Execute multiple tools
```bash
curl -X POST http://localhost:8000/batch \
  -H "Content-Type: application/json" \
  -d '[
    {"tool_name": "calculator", "arguments": {"expression": "50+50"}},
    {"tool_name": "get_time", "arguments": {}}
  ]'

Response:
{
  "results": [
    {"tool_name": "calculator", "result": "100", "success": true},
    {"tool_name": "get_time", "result": "2025-01-15 14:30:45", "success": true}
  ],
  "count": 2
}
```

### Tool Definitions

**calculator(expression)**
- Input: Mathematical expression (string)
- Output: Result (string)
- Example: "100 * 0.02" → "2.0"

**read_file(path)**
- Input: File path (string)
- Output: File contents up to 1000 chars
- Example: "data.json" → file content

**write_file(path, content)**
- Input: File path, content
- Output: Success message
- Example: write to "output.txt"

**get_time()**
- Input: None
- Output: Current date/time
- Example: "2025-01-15 14:30:45"

**search_rag(query)**
- Input: Search query (string)
- Output: Top 3 matching documents
- Example: "trading strategies" → relevant docs

---

## VERIFICATION CHECKLIST

Run this after setup to verify everything works:

```bash
# 1. Check Ollama
curl http://localhost:11434/api/tags
# Should return: {"models": [...]}

# 2. Check Python imports
python -c "from langchain.agents import AgentExecutor; print('✓')"
python -c "from chromadb import Client; print('✓')"
python -c "from fastapi import FastAPI; print('✓')"

# 3. Start MCP Server (Terminal 1)
python mcp_server.py &
sleep 2

# 4. Check MCP endpoint
curl http://localhost:8000/health
# Should return: {"status":"ok","service":"MCP Server"}

# 5. Test calculator tool
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"calculator","arguments":{"expression":"2+2"}}'
# Should return: {"tool_name":"calculator","result":"4","success":true}

# 6. Run agent (Terminal 2)
timeout 30 python agent.py < /dev/null
# Should show example tasks

# 7. Run client tests (Terminal 3)
python mcp_client.py
# Should show all tests passing

# 8. Run RAG tests
python -c "from rag import RAGSystem; r = RAGSystem(); print('✓ RAG initialized')"
```

**✓ If all above pass:** System is working correctly

---

## TROUBLESHOOTING

### "Ollama not running"
```bash
# Verify Ollama is listening
curl http://localhost:11434/api/tags

# If not, start it
/Applications/Ollama.app/Contents/MacOS/Ollama serve
# or
open /Applications/Ollama.app
```

### "ModuleNotFoundError: No module named 'langchain'"
```bash
source venv/bin/activate
pip install -r requirements.txt
python -c "import langchain; print(langchain.__version__)"
```

### "Connection refused on port 8000"
```bash
# Check if something is using port 8000
lsof -i :8000

# Kill it if needed
kill -9 <PID>

# Restart MCP server
python mcp_server.py
```

### "Port 8000 already in use"
```bash
# Find what's using it
netstat -tuln | grep 8000

# Use a different port
# Edit mcp_server.py line: uvicorn.run(..., port=8001)
```

### "Agent is very slow"
```bash
# Reduce iterations (in agent.py)
max_iterations=3  # Change from 5 to 3
# or reduce temperature
temperature=0.1  # Lower = faster, more deterministic
```

### "gemma4:e4b not found"
```bash
# Pull the model
ollama pull gemma4:e4b

# Verify
ollama list
# Should show: gemma4:e4b
```

### "Chroma database issues"
```bash
# Reset vector DB (will lose data)
rm -rf data/chroma_db

# Reinitialize
python rag.py
```

---

## REAL WORLD EXAMPLES

### Example 1: Trading Profit Calculation
```
You: Calculate my trading profit: Entry at 100, Exit at 105, Quantity 10

Agent:
1. Thinks: "I need to calculate (105-100) * 10"
2. Uses: calculator tool
3. Calculates: (105-100) * 10 = 50
4. Returns: "Your profit is 50"
```

### Example 2: Search Knowledge Base
```
You: What's my long straddle strategy?

Agent:
1. Thinks: "User is asking about a strategy"
2. Uses: search_rag tool
3. Searches: "long straddle strategy"
4. Retrieves: Relevant sections from trading.md
5. Returns: Strategy details from knowledge base
```

### Example 3: Create & Analyze File
```
You: Create a JSON file with my trading setup, then read it back

Agent:
1. Uses: write_file tool
2. Creates: trading_setup.json
3. Uses: read_file tool
4. Reads: Contents of trading_setup.json
5. Returns: File content
```

### Example 4: Test via API
```bash
# Test MCP server without agent
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "write_file",
    "arguments": {
      "file_path": "test.json",
      "content": "{\"status\": \"test\"}"
    }
  }'

# Server handles it, returns success
```

---

## NEXT STEPS

### Today (Done!)
- ✅ Generate project with Claude Code
- ✅ Setup environment
- ✅ Run Agent + RAG + MCP
- ✅ Verify everything works

### Tomorrow
- Add your own tools to agent.py
- Add your own documents to data/docs/
- Customize agent behavior

### Next Week
- Deploy MCP server (AWS/Heroku)
- Add streaming responses
- Build frontend UI
- Integrate with Claude.ai

### Next Month
- Add memory/conversation history
- Implement hybrid search (BM25 + semantic)
- Scale to multiple documents
- Add authentication

---

## COMMIT THIS FILE TO GIT

After generating the project, commit this file:

```bash
git add INSTRUCTIONS.md
git commit -m "docs: add comprehensive setup and build instructions"
```

This file can be referenced when:
- Setting up the project
- Onboarding new team members
- Troubleshooting issues
- Deploying to production

---

## QUICK COMMANDS REFERENCE

```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python rag.py

# Run components
python mcp_server.py      # Terminal 1
python agent.py           # Terminal 2
python mcp_client.py      # Terminal 3

# Test MCP
curl http://localhost:8000/health
curl http://localhost:8000/tools
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"calculator","arguments":{"expression":"2+2"}}'

# Git operations
git init
git add .
git commit -m "initial commit"
git log --oneline
```

---

## SUPPORT & RESOURCES

**For Claude Code:**
- https://claude.ai
- Claude Desktop App

**For Technologies:**
- Ollama: https://ollama.ai
- LangChain: https://python.langchain.com
- FastAPI: https://fastapi.tiangolo.com
- Chroma: https://docs.trychroma.com

**For Issues:**
- Check Troubleshooting section above
- Verify Ollama is running
- Check Python version (3.9+)
- Verify port 8000 is available

---

## LICENSE & ATTRIBUTION

This is a POC project built for local AI experimentation with:
- Ollama (open source)
- LangChain (open source)
- Chroma (open source)
- FastAPI (open source)

---

**Ready to build? Follow the Quick Start section above.**

**Time to working system: 30 minutes ✓**
