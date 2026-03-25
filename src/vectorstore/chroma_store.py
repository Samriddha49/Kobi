"""ChromaDB vector store integration for the Poetry RAG Critic.

Handles:
- Embedding poems using all-MiniLM-L6-v2 (sentence-transformers)
- Persisting to / loading from a local ChromaDB directory
- Providing a LangChain retriever for similarity search
"""

from __future__ import annotations

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from config import (
    CHROMA_COLLECTION_NAME,
    CHROMA_PERSIST_DIR,
    EMBEDDING_MODEL,
    RETRIEVAL_TOP_K,
)
from src.ingestion.pdf_loader import load_all_poems
from src.ingestion.poetry_splitter import PoetryStanzaSplitter


def _get_embeddings() -> HuggingFaceEmbeddings:
    """Return the configured sentence-transformers embedding function."""
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vectorstore() -> Chroma:
    """Ingest all poem PDFs, chunk them, embed, and persist to ChromaDB.

    If the collection already exists and has documents, this is a no-op
    so the expensive embedding step is not repeated on every app restart.
    """
    embeddings = _get_embeddings()

    # Try to open an existing store first
    store = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )

    # Skip re-ingestion if documents are already present
    if store._collection.count() > 0:
        return store

    # ── First-time ingestion ───────────────────────────────────────────
    documents = load_all_poems()
    if not documents:
        return store  # nothing to ingest yet

    splitter = PoetryStanzaSplitter(min_stanza_lines=2)
    chunks = splitter.split_documents(documents)

    store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=CHROMA_PERSIST_DIR,
    )

    return store


def get_retriever(store: Chroma | None = None):
    """Return a LangChain retriever backed by the ChromaDB store.

    Parameters
    ----------
    store : Chroma, optional
        An already-initialised Chroma store.  If *None*, one is built /
        loaded automatically.
    """
    if store is None:
        store = build_vectorstore()

    return store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": RETRIEVAL_TOP_K},
    )
