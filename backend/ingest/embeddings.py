from __future__ import annotations

import json

import boto3

from .config import IngestConfig


def get_bedrock_client(cfg: IngestConfig):
  return boto3.client("bedrock-runtime", region_name=cfg.aws_region)


def embed_texts(cfg: IngestConfig, texts: list[str]) -> list[list[float]]:
  """
  Embed a list of texts using Amazon Titan Text Embeddings v2.

  For learning and simplicity we call the model once per text.
  """
  client = get_bedrock_client(cfg)
  embeddings: list[list[float]] = []

  for text in texts:
    body = {
      "inputText": text,
      "dimensions": 1024,  # must match vector_dimension in terraform
    }
    response = client.invoke_model(
      modelId=cfg.bedrock_embed_model_id,
      body=json.dumps(body).encode("utf-8"),
      contentType="application/json",
    )
    payload = json.loads(response["body"].read())
    vector = payload["embedding"]
    embeddings.append(vector)

  return embeddings