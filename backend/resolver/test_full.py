"""
Integration tests for the resolver: require AWS credentials and env (VECTOR_* , BEDROCK_*).
Skip when env not set or --no-integration passed.
"""

from __future__ import annotations

import os

import pytest

from ingest.config import load_config
from resolver.agent import resolve


def _has_resolver_env() -> bool:
    return bool(os.getenv("VECTOR_BUCKET_NAME") and os.getenv("AWS_REGION"))


@pytest.mark.skipif(not _has_resolver_env(), reason="VECTOR_BUCKET_NAME and AWS_REGION not set")
def test_resolve_returns_draft_and_sources() -> None:
    cfg = load_config()
    result = resolve("How do I reset my password?", "I lost access to my email.", cfg=cfg, top_k=2)
    assert "draft" in result
    assert isinstance(result["draft"], str)
    assert "sources" in result
    assert isinstance(result["sources"], list)
    assert result["policy_ok"] is True
