from __future__ import annotations

from collections.abc import Iterable, Mapping

import boto3

from .config import IngestConfig


def get_s3vectors_client(cfg: IngestConfig):
  return boto3.client("s3vectors", region_name=cfg.aws_region)


def put_vectors(
  cfg: IngestConfig,
  vectors: Iterable[tuple[str, list[float], Mapping[str, str]]],
) -> None:
  """
  Write vectors into the S3 Vectors index.

  vectors: iterable of (key, embedding, metadata_dict)
  """
  client = get_s3vectors_client(cfg)

  payload_vectors = []
  for key, embedding, metadata in vectors:
    payload_vectors.append(
      {
        "key": key,
        "data": {"float32": [float(x) for x in embedding]},
        "metadata": dict(metadata),
      }
    )

  if not payload_vectors:
    return

  client.put_vectors(
    vectorBucketName=cfg.vector_bucket_name,
    indexName=cfg.vector_index_name,
    vectors=payload_vectors,
  )


def query_vectors(
  cfg: IngestConfig,
  query_embedding: list[float],
  top_k: int = 10,
  return_metadata: bool = True,
  return_distance: bool = True,
) -> list[dict]:
  """
  Run similarity search: find the top_k nearest vectors to query_embedding.

  Returns list of hits, each with key, optional distance, optional metadata.
  """
  client = get_s3vectors_client(cfg)
  response = client.query_vectors(
    vectorBucketName=cfg.vector_bucket_name,
    indexName=cfg.vector_index_name,
    topK=top_k,
    queryVector={"float32": [float(x) for x in query_embedding]},
    returnDistance=return_distance,
    returnMetadata=return_metadata,
  )
  return response.get("vectors", [])