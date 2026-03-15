"""
Run the resolver on a ticket (title + description).

  uv run python -m resolver.run_resolve
  uv run python -m resolver.run_resolve "Password reset" "I cannot log in..."
"""

from __future__ import annotations

import sys

from .agent import resolve


def main() -> None:
  title = "Sample ticket"
  body = "Customer cannot reset password; forgot email."
  if len(sys.argv) >= 3:
    title = sys.argv[1]
    body = " ".join(sys.argv[2:])
  elif len(sys.argv) == 2:
    body = sys.argv[1]

  print("Resolving ticket...")
  result = resolve(title, body)
  print("\n--- Draft ---")
  print(result["draft"])
  print("\n--- Sources (top chunks) ---")
  for i, s in enumerate(result["sources"], 1):
    print(f"  {i}. {s.get('text', '')[:80]}...")
  print(f"\nPolicy OK: {result['policy_ok']}")


if __name__ == "__main__":
  main()
