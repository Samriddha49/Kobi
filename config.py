"""Central configuration for the Poetry RAG Critic application."""

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MY_POEMS_DIR = DATA_DIR / "my_poems"
PUBLIC_POEMS_DIR = DATA_DIR / "public_poems"
CHROMA_PERSIST_DIR = str(BASE_DIR / "chroma_db")

# ── Models ─────────────────────────────────────────────────────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "phi3"

# ── Ollama ─────────────────────────────────────────────────────────────
OLLAMA_BASE_URL = "http://localhost:11434"

# ── Retrieval ──────────────────────────────────────────────────────────
CHROMA_COLLECTION_NAME = "poetry_rag"
RETRIEVAL_TOP_K = 5

# ── Retry settings ────────────────────────────────────────────────────
MAX_RETRIES = 3
RETRY_WAIT_SECONDS = 5  # initial back-off
