# TicketResolve

Agentic AI support ticket resolution system: Bedrock, S3 Vectors, and a simple web UI. Built step-by-step for learning.

## Overview

TicketResolve uses a single **resolver** agent that searches a knowledge base and past tickets, drafts a response, and checks policy before returning a suggested resolution. Data lives in S3 Vectors; the API is FastAPI; infra is Terraform per component.

- **Repo layout and plan**: [gameplan.md](gameplan.md)
- **Step-by-step guides**: [guides/](guides/) — start with [1_permissions.md](guides/1_permissions.md)

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Python 3.11+
- AWS account and CLI configured (see Guide 1)

## Quick start

1. Clone the repo and open [gameplan.md](gameplan.md).
2. Follow the guides in order: **1_permissions** → **2_vectors_ingest** → **3_agents** → **4_frontend**.
3. Work through one guide (or one day) at a time; don’t skip ahead.

## Structure

```
ticketresolve/
├── gameplan.md       # Project briefing and learning path
├── guides/           # Numbered deployment guides
├── backend/          # Python uv workspace (api, resolver, ingest)
├── frontend/         # Simple single-page UI
├── terraform/        # Per-component infra
└── scripts/          # deploy, destroy, run_local
```

## CI/CD

GitHub Actions runs on push and PRs:

- **CI**: Lint (Ruff) and tests (pytest) for the backend. See [.github/workflows/ci.yml](.github/workflows/ci.yml).

## License

MIT (or add your chosen license file.)
