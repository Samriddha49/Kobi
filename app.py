"""Poetry RAG Critic — Streamlit Application.

A web interface for submitting poems and receiving AI-generated literary
critiques powered by a Retrieval-Augmented Generation pipeline.
"""

import streamlit as st

from src.chain.critique_chain import build_critique_chain, invoke_critique
from src.vectorstore.chroma_store import build_vectorstore


# ── Page configuration ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Poetry RAG Critic",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Main background & text */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.85);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Elegant title */
    .main-title {
        font-family: 'Georgia', serif;
        font-size: 2.8rem;
        background: linear-gradient(90deg, #f5af19, #f12711, #f5af19);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: 2px;
    }
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.55);
        font-size: 1.05rem;
        margin-bottom: 2rem;
        font-style: italic;
    }

    /* Critique output card */
    .critique-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 2rem;
        backdrop-filter: blur(12px);
        margin-top: 1.5rem;
        color: #e0e0e0;
        line-height: 1.75;
    }

    /* Text area */
    .stTextArea textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        color: #f0f0f0 !important;
        border-radius: 12px !important;
        font-family: 'Georgia', serif !important;
        font-size: 1.05rem !important;
        line-height: 1.8 !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #f5af19, #f12711) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 2.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(245, 175, 25, 0.4) !important;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #f5af19 !important;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] .stMarkdown {
        color: rgba(255,255,255,0.75);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📖 About")
    st.markdown(
        "**Poetry RAG Critic** uses a Retrieval-Augmented Generation "
        "pipeline to deliver constructive literary critiques of your poems.\n\n"
        "The AI draws on a dual knowledge base of original works and "
        "classic public-domain poetry to ground its analysis in real "
        "literary tradition."
    )
    st.divider()
    st.markdown("### How it works")
    st.markdown(
        "1. Paste or type your poem below.\n"
        "2. Click **✨ Get Critique**.\n"
        "3. The system retrieves similar stanzas from its knowledge base, "
        "then generates a structured critique covering form, imagery, "
        "theme, strengths, and suggestions."
    )
    st.divider()
    st.markdown(
        "⚙️ *Powered by LangChain · phi3 (Ollama) · ChromaDB*",
        help="Running locally via Ollama — make sure Ollama is running with the mistral model pulled.",
    )


# ── Initialise vector store & chain (cached) ──────────────────────────
@st.cache_resource(show_spinner="Initialising knowledge base …")
def _init_chain():
    """Build the vector store and critique chain once; cache across reruns."""
    store = build_vectorstore()
    if store._collection.count() == 0:
        return None  # no poems ingested
    from src.vectorstore.chroma_store import get_retriever

    retriever = get_retriever(store)
    return build_critique_chain(retriever)


chain = _init_chain()


# ── Main content ───────────────────────────────────────────────────────
st.markdown('<h1 class="main-title">Poetry RAG Critic</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Submit a poem and receive a thoughtful, AI-powered literary critique</p>',
    unsafe_allow_html=True,
)

if chain is None:
    st.warning(
        "⚠️ **No poems found in the knowledge base.**  "
        "Please add PDF files to `data/my_poems/` and `data/public_poems/`, "
        "then restart the app."
    )
    st.stop()

# Poem input
poem_text = st.text_area(
    "📝 Your Poem",
    height=280,
    placeholder="Paste or type your poem here …\n\nStanza breaks (blank lines) are preserved.",
    key="poem_input",
)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    submit = st.button("✨ Get Critique", use_container_width=True)

# ── Critique generation ───────────────────────────────────────────────
if submit:
    if not poem_text or not poem_text.strip():
        st.error("Please enter a poem before requesting a critique.")
    else:
        with st.spinner("Analysing your poem — this may take a moment …"):
            try:
                critique = invoke_critique(chain, poem_text.strip())
                st.markdown("---")
                st.markdown("### 🎭 Literary Critique")
                st.markdown(
                    f'<div class="critique-card">{critique}</div>',
                    unsafe_allow_html=True,
                )
            except Exception as exc:
                error_msg = str(exc).lower()
                if "connection" in error_msg or "refused" in error_msg:
                    st.error(
                        "🔌 **Cannot connect to Ollama.**  "
                        "Make sure Ollama is running (`ollama serve`) and the "
                        "Mistral model is pulled (`ollama pull mistral`)."
                    )
                elif "model" in error_msg and "not found" in error_msg:
                    st.error(
                        "📦 **Mistral model not found.**  "
                        "Run `ollama pull mistral` to download it first."
                    )
                else:
                    st.error(
                        f"❌ **Something went wrong:**  \n`{exc}`\n\n"
                        "Please try again or check the logs for details."
                    )
