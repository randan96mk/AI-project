"""
MCP Server - FastAPI HTTP server exposing agent tools via REST API.
Endpoints: GET /health, GET /tools, POST /call, POST /batch
"""

import logging
from typing import Any, Dict, List

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent import calculator, get_time, read_file, search_rag, write_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MCP Server", description="Model Context Protocol HTTP API", version="1.0.0")

# ── Pydantic models ───────────────────────────────────────────────────────────

class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any] = {}


class ToolResult(BaseModel):
    tool_name: str
    result: str
    success: bool


class BatchResult(BaseModel):
    results: List[ToolResult]
    count: int


# ── Tool registry ─────────────────────────────────────────────────────────────

TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {
    "calculator": {
        "description": "Evaluate a mathematical expression",
        "parameters": {"expression": "string - math expression e.g. '2+2'"},
        "fn": lambda args: calculator(args.get("expression", "")),
    },
    "read_file": {
        "description": "Read file contents (first 1000 chars)",
        "parameters": {"path": "string - file path"},
        "fn": lambda args: read_file(args.get("path", "")),
    },
    "write_file": {
        "description": "Write content to a file. Args: file_path and content.",
        "parameters": {
            "file_path": "string - destination file path",
            "content": "string - content to write",
        },
        "fn": lambda args: write_file(f"{args.get('file_path', '')}|||{args.get('content', '')}"),
    },
    "get_time": {
        "description": "Get the current date and time",
        "parameters": {},
        "fn": lambda _args: get_time(),
    },
    "search_rag": {
        "description": "Search the knowledge base for relevant documents",
        "parameters": {"query": "string - search query"},
        "fn": lambda args: search_rag(args.get("query", "")),
    },
}


def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> ToolResult:
    """
    Execute a registered tool by name.

    Args:
        tool_name: Name of the tool to execute.
        arguments: Dict of arguments to pass to the tool.

    Returns:
        ToolResult with result string and success flag.
    """
    if tool_name not in TOOL_REGISTRY:
        return ToolResult(tool_name=tool_name, result=f"Unknown tool: {tool_name}", success=False)
    try:
        result = TOOL_REGISTRY[tool_name]["fn"](arguments)
        logger.info("Tool '%s' executed successfully", tool_name)
        return ToolResult(tool_name=tool_name, result=str(result), success=True)
    except Exception as exc:
        logger.error("Tool '%s' failed: %s", tool_name, exc)
        return ToolResult(tool_name=tool_name, result=f"Error: {exc}", success=False)


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
def health() -> Dict[str, str]:
    """Return server health status."""
    return {"status": "ok", "service": "MCP Server"}


@app.get("/tools")
def list_tools() -> Dict[str, Any]:
    """List all available tools with descriptions and parameters."""
    tools = [
        {
            "name": name,
            "description": meta["description"],
            "parameters": meta["parameters"],
        }
        for name, meta in TOOL_REGISTRY.items()
    ]
    return {"tools": tools, "count": len(tools)}


@app.post("/call", response_model=ToolResult)
def call_tool(request: ToolCall) -> ToolResult:
    """
    Execute a single tool call.

    Args:
        request: ToolCall with tool_name and arguments.

    Returns:
        ToolResult with result and success flag.
    """
    logger.info("POST /call | tool=%s | args=%s", request.tool_name, request.arguments)
    result = execute_tool(request.tool_name, request.arguments)
    if not result.success and "Unknown tool" in result.result:
        raise HTTPException(status_code=404, detail=result.result)
    return result


@app.post("/batch", response_model=BatchResult)
def batch_call(requests: List[ToolCall]) -> BatchResult:
    """
    Execute multiple tool calls in sequence.

    Args:
        requests: List of ToolCall objects.

    Returns:
        BatchResult with list of ToolResults and count.
    """
    logger.info("POST /batch | %d tools", len(requests))
    results = [execute_tool(req.tool_name, req.arguments) for req in requests]
    return BatchResult(results=results, count=len(results))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
