# ── Build stage ─────────────────────────────────────────────────────────
FROM python:3.11-slim AS base

WORKDIR /app

# Install OS‑level deps (none beyond what slim provides, but keeps layer cacheable)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python deps — cached unless requirements change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .

# Streamlit configuration: disable telemetry and file‑watcher for Docker
RUN mkdir -p /root/.streamlit && \
    echo "[server]\nheadless = true\nport = 8501\nenableCORS = false\nenableXsrfProtection = false\n\n[browser]\ngatherUsageStats = false" \
    > /root/.streamlit/config.toml

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
