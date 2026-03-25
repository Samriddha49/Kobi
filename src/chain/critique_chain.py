"""LangChain critique chain with Mistral (Ollama) LLM and retry logic.

Builds an LCEL (LangChain Expression Language) chain:
    retriever -> prompt -> Phi3 LLM (via Ollama) -> string output
with tenacity-based retry / exponential backoff for resilience.
"""

from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from config import LLM_MODEL, MAX_RETRIES, OLLAMA_BASE_URL, RETRY_WAIT_SECONDS
from src.chain.prompts import CRITIQUE_PROMPT
from src.vectorstore.chroma_store import get_retriever


def _format_docs(docs) -> str:
    """Concatenate retrieved documents into a single context string."""
    parts: list[str] = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("filename", "unknown")
        corpus = doc.metadata.get("corpus", "unknown")
        parts.append(
            f"[Reference {i} — {source} ({corpus})]\n{doc.page_content}"
        )
    return "\n\n---\n\n".join(parts)


def _get_llm() -> ChatOllama:
    """Return the configured Mistral chat model via Ollama."""
    return ChatOllama(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.7,
    )


def build_critique_chain(retriever=None):
    """Construct the full RAG chain.

    Parameters
    ----------
    retriever : optional
        A pre-built retriever.  If *None*, one is created from the
        persisted ChromaDB store.

    Returns
    -------
    runnable
        An LCEL chain that accepts ``{"question": "..."}`` and returns
        the critique as a plain string.
    """
    if retriever is None:
        retriever = get_retriever()

    llm = _get_llm()

    chain = (
        {
            "context": retriever | _format_docs,
            "question": RunnablePassthrough(),
        }
        | CRITIQUE_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain


# ── Retry-safe invocation ──────────────────────────────────────────────

@retry(
    retry=retry_if_exception_type(Exception),
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=RETRY_WAIT_SECONDS, min=2, max=60),
    reraise=True,
)
def invoke_critique(chain, poem_text: str) -> str:
    """Invoke the critique chain with automatic retries on failure.

    Raises the underlying exception after ``MAX_RETRIES`` attempts.
    """
    return chain.invoke(poem_text)
