from __future__ import annotations

import os

import boto3

from ingest.config import IngestConfig, load_config

from .templates import SYSTEM_PROMPT, user_message
from .tools import knowledge_search, policy_checker


def get_chat_model_id() -> str:
  return os.getenv("BEDROCK_CHAT_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")


def draft_reply(cfg: IngestConfig, model_id: str, user_prompt: str) -> str:
  """Call Bedrock Converse API with system + user message; return assistant text."""
  client = boto3.client("bedrock-runtime", region_name=cfg.aws_region)
  response = client.converse(
    modelId=model_id,
    system=[{"text": SYSTEM_PROMPT}],
    messages=[{"role": "user", "content": [{"text": user_prompt}]}],
    inferenceConfig={"maxTokens": 1024, "temperature": 0.3},
  )
  output = response.get("output", {})
  message = output.get("message", {})
  parts = message.get("content", [])
  texts = [p["text"] for p in parts if "text" in p]
  return "\n".join(texts).strip() if texts else ""


def resolve(
  ticket_title: str,
  ticket_description: str,
  *,
  cfg: IngestConfig | None = None,
  top_k: int = 5,
) -> dict:
  """
  Run the resolver flow: optional knowledge search → Bedrock draft → optional policy check.
  Returns dict with keys: draft, sources, policy_ok.
  """
  if cfg is None:
    cfg = load_config()

  query = f"{ticket_title}\n{ticket_description}".strip()
  sources = knowledge_search(cfg, query, top_k=top_k)
  prompt = user_message(ticket_title, ticket_description, sources)
  model_id = get_chat_model_id()
  draft = draft_reply(cfg, model_id, prompt)
  policy_ok = policy_checker(draft)

  return {
    "draft": draft,
    "sources": sources,
    "policy_ok": policy_ok,
  }
