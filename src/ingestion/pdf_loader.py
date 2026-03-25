"""PDF ingestion and preprocessing for the Poetry RAG Critic.

Loads all .pdf files from the two corpus directories, strips common PDF
artifacts (page numbers, headers, footers), and returns clean LangChain
Document objects with corpus metadata.
"""

import re
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from config import MY_POEMS_DIR, PUBLIC_POEMS_DIR


# ── Preprocessing ──────────────────────────────────────────────────────

def _clean_text(raw: str) -> str:
    """Strip common PDF artifacts from extracted text.

    Removes:
    - Standalone page numbers (e.g. "  3  " on their own line)
    - Repeated header / footer lines (short lines that look like titles)
    - Excessive blank lines (collapsed to double‑newline)
    """
    lines = raw.splitlines()
    cleaned: list[str] = []

    for line in lines:
        stripped = line.strip()

        # Skip standalone page numbers
        if re.fullmatch(r"\d{1,4}", stripped):
            continue

        # Skip very short lines that are likely headers/footers
        # (e.g. "Page 3 of 10", "Draft — Confidential")
        if re.fullmatch(r"(page\s+\d+(\s+of\s+\d+)?|draft.*|confidential.*)", stripped, re.IGNORECASE):
            continue

        cleaned.append(line)

    text = "\n".join(cleaned)
    # Collapse runs of 3+ blank lines into exactly 2 (stanza break)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ── Loader ─────────────────────────────────────────────────────────────

def _load_pdfs_from_dir(directory: Path, corpus_label: str) -> List[Document]:
    """Load and preprocess every PDF in *directory*.

    Each returned Document carries metadata:
        - ``source``: original file path
        - ``corpus``: ``"my_poems"`` or ``"public_poems"``
        - ``filename``: basename of the PDF
    """
    docs: List[Document] = []
    pdf_files = sorted(directory.glob("*.pdf"))

    if not pdf_files:
        return docs

    for pdf_path in pdf_files:
        loader = PyPDFLoader(str(pdf_path))
        raw_docs = loader.load()

        # Merge all pages of one PDF into a single text block
        full_text = "\n".join(page.page_content for page in raw_docs)
        cleaned = _clean_text(full_text)

        if cleaned:
            docs.append(
                Document(
                    page_content=cleaned,
                    metadata={
                        "source": str(pdf_path),
                        "corpus": corpus_label,
                        "filename": pdf_path.name,
                    },
                )
            )

    return docs


def load_all_poems() -> List[Document]:
    """Load and preprocess poems from **both** corpus directories.

    Returns a flat list of ``Document`` objects ready for chunking.
    """
    my_poems = _load_pdfs_from_dir(MY_POEMS_DIR, "my_poems")
    public_poems = _load_pdfs_from_dir(PUBLIC_POEMS_DIR, "public_poems")
    return my_poems + public_poems
