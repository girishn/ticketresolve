"""
Query the S3 Vectors index by embedding a search string and returning similar items.

Run from backend/:  uv run python -m ingest.query_text
Optional:  uv run python -m ingest.query_text "your search question here"
"""

from __future__ import annotations

import sys

from .config import load_config
from .embeddings import embed_texts
from .s3vectors_client import query_vectors


def main() -> None:
    cfg = load_config()

    query = "How do I reset my password?"
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])

    print(f"Query: {query}")
    print("Embedding query with Bedrock...")
    [query_embedding] = embed_texts(cfg, [query])

    print("Searching S3 Vectors index...")
    hits = query_vectors(cfg, query_embedding, top_k=5)

    print(f"\nFound {len(hits)} result(s):\n")
    for i, hit in enumerate(hits, 1):
        key = hit.get("key", "?")
        dist = hit.get("distance")
        meta = hit.get("metadata") or {}
        text_preview = meta.get("text", meta.get("source", ""))
        print(f"  {i}. key={key}" + (f"  distance={dist:.4f}" if dist is not None else ""))
        if text_preview:
            preview = text_preview[:80] + "..." if len(text_preview) > 80 else text_preview
            print(f"     {preview}")
        print()


if __name__ == "__main__":
    main()
