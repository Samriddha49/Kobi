"""Custom stanza‑aware text splitter for poetry.

Instead of splitting on character counts (which destroys poetic form),
this splitter chunks strictly on stanza boundaries (double‑newline gaps)
and preserves the original line breaks within each stanza.
"""

from __future__ import annotations

import re
from typing import Any, List

from langchain_core.documents import Document
from langchain_text_splitters import TextSplitter


class PoetryStanzaSplitter(TextSplitter):
    """Split poems on stanza breaks (blank‑line boundaries).

    Parameters
    ----------
    min_stanza_lines : int
        If a stanza has fewer lines than this, it is merged with the
        next stanza to avoid tiny, context‑free chunks.  Default ``2``.
    """

    def __init__(self, min_stanza_lines: int = 2, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.min_stanza_lines = min_stanza_lines

    # ── Core override ──────────────────────────────────────────────────

    def split_text(self, text: str) -> List[str]:
        """Return a list of stanza chunks from *text*."""
        # Normalise line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Split on one or more blank lines (stanza breaks)
        raw_stanzas = re.split(r"\n\s*\n", text)

        # Strip each stanza but keep internal line breaks
        stanzas = [s.strip() for s in raw_stanzas if s.strip()]

        if not stanzas:
            return []

        # Merge very small stanzas with the following one
        merged: List[str] = []
        buffer = ""
        for stanza in stanzas:
            if buffer:
                buffer += "\n\n" + stanza
            else:
                buffer = stanza

            line_count = len(buffer.strip().splitlines())
            if line_count >= self.min_stanza_lines:
                merged.append(buffer.strip())
                buffer = ""

        # Flush remaining buffer
        if buffer.strip():
            if merged:
                merged[-1] += "\n\n" + buffer.strip()
            else:
                merged.append(buffer.strip())

        return merged

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split each document into stanza‑level chunks, preserving metadata."""
        chunks: List[Document] = []
        for doc in documents:
            stanza_texts = self.split_text(doc.page_content)
            for i, stanza in enumerate(stanza_texts):
                chunks.append(
                    Document(
                        page_content=stanza,
                        metadata={
                            **doc.metadata,
                            "stanza_index": i,
                        },
                    )
                )
        return chunks
