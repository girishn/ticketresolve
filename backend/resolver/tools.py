from __future__ import annotations

from ingest.config import IngestConfig
from ingest.embeddings import embed_texts
from ingest.s3vectors_client import query_vectors


def knowledge_search(cfg: IngestConfig, query: str, top_k: int = 5) -> list[dict]:
    """
    Embed the query, run vector search, and return hits with metadata (e.g. text, distance).
    """
    if not query.strip():
        return []
    embeddings = embed_texts(cfg, [query])
    hits = query_vectors(
        cfg, embeddings[0], top_k=top_k, return_metadata=True, return_distance=True
    )
    # Normalize for templates: each chunk has "text" (from metadata or key) and optional "distance"
    chunks = []
    for h in hits:
        meta = h.get("metadata") or {}
        text = meta.get("text") or h.get("key") or ""
        chunks.append({"text": text, "distance": h.get("distance")})
    return chunks


def ticket_history(_cfg: IngestConfig, _ticket_id: str) -> list[dict]:
    """
    Placeholder: return prior messages/updates for this ticket.
    In v1 we do not have a ticket DB; can reuse knowledge_search with a ticket-scoped query later.
    """
    return []


def policy_checker(_draft: str) -> bool:
    """
    Placeholder: return True if the draft passes policy/tone checks.
    Later: optional LLM or rules-based check.
    """
    return True
