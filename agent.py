"""
Autonomous AI Agent using LangChain ReAct pattern with Ollama (gemma4:e4b).
Tools: calculator, read_file, write_file, get_time, search_rag.
"""

import datetime
import logging
from typing import Any

from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain_community.llms import Ollama

from rag import RAGSystem

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

OLLAMA_MODEL = "gemma4:e4b"
OLLAMA_BASE_URL = "http://localhost:11434"

_rag_system: RAGSystem | None = None


def _get_rag() -> RAGSystem:
    global _rag_system
    if _rag_system is None:
        _rag_system = RAGSystem()
    return _rag_system


# ── Tool implementations ──────────────────────────────────────────────────────

def calculator(expression: str) -> str:
    """
    Evaluate a safe mathematical expression.

    Args:
        expression: Math expression string, e.g. '2 + 2' or '100 * 0.02'.

    Returns:
        String representation of the result.

    Raises:
        ValueError: If expression contains unsafe code.
    """
    allowed = set("0123456789+-*/().% \t")
    if not all(c in allowed for c in expression):
        raise ValueError(f"Unsafe expression: {expression}")
    try:
        result = eval(expression, {"__builtins__": {}})  # noqa: S307
        return str(result)
    except Exception as exc:
        return f"Error evaluating expression: {exc}"


def read_file(path: str) -> str:
    """
    Read the first 1000 characters of a file.

    Args:
        path: Relative or absolute file path.

    Returns:
        File contents (up to 1000 chars) or an error message.
    """
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read(1000)
        return content if content else "(empty file)"
    except FileNotFoundError:
        return f"Error: File not found: {path}"
    except Exception as exc:
        return f"Error reading file: {exc}"


def write_file(args: str) -> str:
    """
    Write content to a file. Expects 'path|||content' format.

    Args:
        args: String in format 'file_path|||content to write'.

    Returns:
        Success or error message.
    """
    try:
        if "|||" not in args:
            return "Error: Expected format 'path|||content'"
        path, content = args.split("|||", 1)
        path = path.strip()
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to {path}"
    except Exception as exc:
        return f"Error writing file: {exc}"


def get_time(_: str = "") -> str:
    """
    Return the current date and time.

    Args:
        _: Unused argument (required by LangChain tool interface).

    Returns:
        Current datetime as a string.
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def search_rag(query: str) -> str:
    """
    Search the knowledge base using RAG similarity search.

    Args:
        query: Natural language query string.

    Returns:
        Formatted string of top matching document chunks.
    """
    try:
        rag = _get_rag()
        results = rag.search(query, k=3)
        if not results:
            return "No relevant documents found."
        parts = []
        for i, r in enumerate(results, 1):
            parts.append(
                f"[Result {i}] (score={r['score']}, source={r['source']})\n{r['content']}"
            )
        return "\n\n".join(parts)
    except RuntimeError:
        return "RAG system not initialized. Run 'python rag.py' first."
    except Exception as exc:
        return f"RAG search error: {exc}"


# ── LangChain tool wrappers ───────────────────────────────────────────────────

TOOLS = [
    Tool(
        name="calculator",
        func=calculator,
        description=(
            "Evaluate a mathematical expression. "
            "Input: math expression string like '2+2' or '100*0.02'. "
            "Output: numeric result as string."
        ),
    ),
    Tool(
        name="read_file",
        func=read_file,
        description=(
            "Read the contents of a file (first 1000 chars). "
            "Input: file path string. Output: file content."
        ),
    ),
    Tool(
        name="write_file",
        func=write_file,
        description=(
            "Write content to a file. "
            "Input format: 'file_path|||content to write'. "
            "Example: 'output.txt|||Hello World'. Output: success message."
        ),
    ),
    Tool(
        name="get_time",
        func=get_time,
        description=(
            "Get the current date and time. "
            "Input: empty string or anything. Output: current datetime."
        ),
    ),
    Tool(
        name="search_rag",
        func=search_rag,
        description=(
            "Search the knowledge base for relevant information. "
            "Input: natural language query. "
            "Output: top 3 matching document excerpts."
        ),
    ),
]

REACT_TEMPLATE = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""


def build_agent() -> AgentExecutor:
    """Build and return a LangChain ReAct AgentExecutor."""
    llm = Ollama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.1,
    )
    prompt = PromptTemplate.from_template(REACT_TEMPLATE)
    agent = create_react_agent(llm, TOOLS, prompt)
    return AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
    )


def run_example_tasks(executor: AgentExecutor) -> None:
    """Run 3 example tasks to demonstrate the agent."""
    examples = [
        "What is 15% of 2500?",
        "What is today's date and time?",
        "Search the knowledge base for NIFTY long straddle strategy.",
    ]
    print("\n" + "=" * 60)
    print("EXAMPLE TASKS")
    print("=" * 60)
    for i, task in enumerate(examples, 1):
        print(f"\n[Example {i}] {task}")
        print("-" * 40)
        try:
            result = executor.invoke({"input": task})
            print(f"Answer: {result['output']}")
        except Exception as exc:
            print(f"Error: {exc}")


def interactive_mode(executor: AgentExecutor) -> None:
    """Run an interactive prompt loop."""
    print("\n" + "=" * 60)
    print("INTERACTIVE MODE  (type 'exit' to quit)")
    print("=" * 60)
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if not user_input or user_input.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break
        try:
            result = executor.invoke({"input": user_input})
            print(f"\nAgent: {result['output']}")
        except Exception as exc:
            print(f"\nError: {exc}")


def main() -> None:
    """Entry point: build agent, run examples, then enter interactive mode."""
    print("Building agent with Ollama model:", OLLAMA_MODEL)
    executor = build_agent()
    run_example_tasks(executor)
    interactive_mode(executor)


if __name__ == "__main__":
    main()
