"""
MCP Client - Test client for the MCP Server HTTP API.
Runs health check, lists tools, tests each tool, and tests batch execution.
"""

import sys
from typing import Any, Dict, List

import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 10


def request(method: str, path: str, json: Any = None) -> Dict[str, Any]:
    """
    Make an HTTP request to the MCP server.

    Args:
        method: HTTP method ('GET' or 'POST').
        path: URL path (e.g. '/health').
        json: Optional JSON body for POST requests.

    Returns:
        Parsed JSON response dict.

    Raises:
        SystemExit: If the server is unreachable.
    """
    url = BASE_URL + path
    try:
        resp = requests.request(method, url, json=json, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        print(f"\nERROR: Cannot connect to MCP server at {BASE_URL}")
        print("Make sure the server is running: python mcp_server.py")
        sys.exit(1)
    except requests.exceptions.HTTPError as exc:
        return {"error": str(exc), "status_code": exc.response.status_code}


def check(label: str, condition: bool, detail: str = "") -> bool:
    """Print a pass/fail line and return the condition."""
    status = "PASS" if condition else "FAIL"
    line = f"  [{status}] {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    return condition


def test_health() -> bool:
    print("\n[1] Health Check")
    data = request("GET", "/health")
    return check("GET /health", data.get("status") == "ok", str(data))


def test_list_tools() -> bool:
    print("\n[2] List Tools")
    data = request("GET", "/tools")
    tools: List[Dict] = data.get("tools", [])
    names = [t["name"] for t in tools]
    ok = check("GET /tools returns tools", len(tools) > 0, f"{len(tools)} tools: {names}")
    expected = {"calculator", "read_file", "write_file", "get_time", "search_rag"}
    ok &= check("All expected tools present", expected.issubset(set(names)))
    return ok


def test_calculator() -> bool:
    print("\n[3] Calculator Tool")
    data = request("POST", "/call", {"tool_name": "calculator", "arguments": {"expression": "2+2"}})
    ok = check("2+2 = 4", data.get("result") == "4" and data.get("success"), str(data))
    data2 = request("POST", "/call", {"tool_name": "calculator", "arguments": {"expression": "100 * 0.02"}})
    ok &= check("100 * 0.02 = 2.0", data2.get("result") == "2.0" and data2.get("success"), str(data2))
    return ok


def test_get_time() -> bool:
    print("\n[4] Get Time Tool")
    data = request("POST", "/call", {"tool_name": "get_time", "arguments": {}})
    ok = data.get("success") and len(data.get("result", "")) > 0
    return check("get_time returns datetime string", ok, data.get("result", ""))


def test_write_read_file() -> bool:
    print("\n[5] Write + Read File Tools")
    write_data = request(
        "POST", "/call",
        {"tool_name": "write_file", "arguments": {"file_path": "test_output.txt", "content": "hello mcp"}}
    )
    ok = check("write_file success", write_data.get("success"), str(write_data))
    read_data = request("POST", "/call", {"tool_name": "read_file", "arguments": {"path": "test_output.txt"}})
    ok &= check("read_file returns content", "hello mcp" in read_data.get("result", ""), str(read_data))
    return ok


def test_search_rag() -> bool:
    print("\n[6] RAG Search Tool")
    data = request(
        "POST", "/call",
        {"tool_name": "search_rag", "arguments": {"query": "NIFTY straddle options strategy"}}
    )
    ok = data.get("success") and len(data.get("result", "")) > 0
    return check("search_rag returns results", ok, data.get("result", "")[:100] + "...")


def test_batch() -> bool:
    print("\n[7] Batch Execution")
    payload = [
        {"tool_name": "calculator", "arguments": {"expression": "50+50"}},
        {"tool_name": "get_time", "arguments": {}},
    ]
    data = request("POST", "/batch", payload)
    results = data.get("results", [])
    ok = check("batch returns 2 results", data.get("count") == 2 and len(results) == 2, str(data))
    ok &= check("calculator in batch = 100", results[0].get("result") == "100" if results else False)
    ok &= check("get_time in batch has value", bool(results[1].get("result")) if len(results) > 1 else False)
    return ok


def main() -> None:
    """Run all tests and print a summary."""
    print("=" * 50)
    print("MCP Client Test Suite")
    print(f"Target: {BASE_URL}")
    print("=" * 50)

    tests = [
        test_health,
        test_list_tools,
        test_calculator,
        test_get_time,
        test_write_read_file,
        test_search_rag,
        test_batch,
    ]

    passed = sum(1 for t in tests if t())
    total = len(tests)

    print("\n" + "=" * 50)
    if passed == total:
        print(f"✓ All {total} tests passed")
    else:
        print(f"✗ {passed}/{total} tests passed")
        sys.exit(1)


if __name__ == "__main__":
    main()
