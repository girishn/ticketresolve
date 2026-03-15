"""
Minimal resolver tests (no Bedrock/S3 calls): templates and tools with mocked config.
"""

from __future__ import annotations

from resolver.templates import SYSTEM_PROMPT, user_message


def test_system_prompt_non_empty() -> None:
    assert len(SYSTEM_PROMPT) > 0
    assert "support" in SYSTEM_PROMPT.lower()


def test_user_message_includes_ticket_and_context() -> None:
    msg = user_message("Reset password", "I forgot my email.", [])
    assert "Reset password" in msg
    assert "I forgot my email." in msg
    assert "Draft a reply" in msg

    msg_with_context = user_message("Bug", "App crashes.", [{"text": "Known issue: fix in v2."}])
    assert "Known issue" in msg_with_context
