from __future__ import annotations

SYSTEM_PROMPT = (
    "You are a helpful support agent. Use the provided knowledge context to draft a "
    "clear, accurate reply to the customer's ticket. If the context does not contain "
    "enough information, say so and suggest next steps (e.g. escalate, ask for more "
    "details). Keep the tone professional and concise."
)


def user_message(ticket_title: str, ticket_description: str, context_chunks: list[dict]) -> str:
  """Build the user prompt: ticket + retrieved knowledge chunks."""
  lines = [
    "## Ticket",
    f"**Title:** {ticket_title}",
    f"**Description:** {ticket_description}",
    "",
  ]
  if context_chunks:
    lines.append("## Relevant knowledge")
    for i, chunk in enumerate(context_chunks, 1):
      text = chunk.get("text") or chunk.get("key", "")
      lines.append(f"{i}. {text}")
    lines.append("")
  lines.append("Draft a reply to this ticket using the knowledge above when relevant.")
  return "\n".join(lines)
