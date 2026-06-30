"""
RAG System - Retrieval-Augmented Generation using Chroma + HuggingFace embeddings.
Loads markdown docs, chunks them, embeds locally, and supports similarity search.
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PERSIST_DIR = "data/chroma_db"
DOCS_DIR = "data/docs"
EMBED_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


class RAGSystem:
    """Retrieval-Augmented Generation system backed by Chroma vector DB."""

    def __init__(self, persist_dir: str = PERSIST_DIR) -> None:
        """
        Initialize the RAG system.

        Args:
            persist_dir: Directory to persist the Chroma vector database.
        """
        self.persist_dir = persist_dir
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        self.vectorstore: Chroma | None = None

        if os.path.exists(persist_dir) and os.listdir(persist_dir):
            logger.info("Loading existing Chroma DB from %s", persist_dir)
            self.vectorstore = Chroma(
                persist_directory=persist_dir,
                embedding_function=self.embeddings,
            )
        else:
            logger.info("No existing DB found. Run load_documents() to initialize.")

    def load_documents(self, docs_path: str = DOCS_DIR) -> int:
        """
        Load markdown files from docs_path, chunk them, and store in Chroma.

        Args:
            docs_path: Directory containing .md files.

        Returns:
            Number of chunks stored.

        Raises:
            FileNotFoundError: If docs_path does not exist.
        """
        path = Path(docs_path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logger.warning("Created empty docs directory at %s", docs_path)

        md_files = list(path.glob("*.md"))
        if not md_files:
            logger.warning("No .md files found in %s", docs_path)
            return 0

        loader = DirectoryLoader(
            docs_path,
            glob="*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        docs = loader.load()
        logger.info("Loaded %d documents", len(docs))

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
        chunks = splitter.split_documents(docs)
        logger.info("Split into %d chunks", len(chunks))

        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_dir,
        )
        self.vectorstore.persist()
        logger.info("Stored and persisted %d chunks to %s", len(chunks), self.persist_dir)
        return len(chunks)

    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Search the vector DB for documents similar to query.

        Args:
            query: Natural language search query.
            k: Number of top results to return.

        Returns:
            List of dicts with keys: content, source, score.

        Raises:
            RuntimeError: If vectorstore is not initialized.
        """
        if self.vectorstore is None:
            raise RuntimeError("Vector store not initialized. Call load_documents() first.")

        results = self.vectorstore.similarity_search_with_score(query, k=k)
        output = []
        for doc, score in results:
            output.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
                "score": round(float(score), 4),
            })
        return output


def main() -> None:
    """Initialize the RAG system by loading sample documents."""
    print("Initializing RAG system...")
    rag = RAGSystem()
    count = rag.load_documents()
    print(f"RAG system ready with {count} chunks.")

    print("\nRunning test search: 'long straddle strategy'")
    results = rag.search("long straddle strategy")
    for i, r in enumerate(results, 1):
        print(f"\n[{i}] Score: {r['score']} | Source: {r['source']}")
        print(r["content"][:200])

    print("\nRAG initialized successfully.")


if __name__ == "__main__":
    main()
