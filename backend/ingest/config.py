from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class IngestConfig:
    aws_region: str
    vector_bucket_name: str
    vector_index_name: str
    bedrock_embed_model_id: str


def load_config() -> IngestConfig:
    """Load ingest configuration from environment variables / .env."""
    aws_region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    if not aws_region:
        raise ValueError("AWS_REGION (or AWS_DEFAULT_REGION) must be set")

    vector_bucket_name = os.getenv("VECTOR_BUCKET_NAME")
    if not vector_bucket_name:
        raise ValueError(
            "VECTOR_BUCKET_NAME must be set (from terraform 2_vectors_ingest output bucket_name)"
        )

    vector_index_name = os.getenv("VECTOR_INDEX_NAME")
    if not vector_index_name:
        raise ValueError(
            "VECTOR_INDEX_NAME must be set (terraform 2_vectors_ingest output vector_index_name)"
        )

    bedrock_model_id = os.getenv("BEDROCK_EMBED_MODEL_ID", "amazon.titan-embed-text-v2:0")

    return IngestConfig(
        aws_region=aws_region,
        vector_bucket_name=vector_bucket_name,
        vector_index_name=vector_index_name,
        bedrock_embed_model_id=bedrock_model_id,
    )
