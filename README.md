# TicketResolve

An agentic AI system that helps resolve support tickets using Amazon Bedrock, S3 Vectors, and a simple web UI. We built it step-by-step so you can follow along and understand how the pieces fit together.

## What this project does

A single **resolver** agent looks up your knowledge base and past tickets, drafts a reply, and runs it through a policy check before suggesting a resolution. Data lives in S3 (with S3 Vectors for embeddings); the app is a FastAPI backend plus a small web UI. Infra is Terraform, one component at a time.

- **The big picture and how we work:** [gameplan.md](gameplan.md)
- **Walkthroughs:** [guides/](guides/) — start with [1_permissions.md](guides/1_permissions.md)

## What you need

- [uv](https://docs.astral.sh/uv/) for Python
- Python 3.11+
- An AWS account and CLI set up (Guide 1 walks you through it)

## Getting started

1. Clone the repo and skim [gameplan.md](gameplan.md) so you know the plan.
2. Do the guides in order: **1_permissions** → **2_vectors_ingest** → **3_agents** → **4_frontend**.
3. Take your time — one guide (or one day) per chunk works better than rushing.

## Repo layout

```
ticketresolve/
├── gameplan.md       # Project plan and how we build it
├── guides/           # Numbered guides (permissions, vectors, agents, frontend)
├── backend/          # Python (uv workspace): api, resolver, ingest
├── frontend/         # Single-page UI
├── terraform/        # Infra per component
└── scripts/          # deploy, destroy, run_local
```

## CI

On push and PRs, GitHub Actions runs lint (Ruff) and tests (pytest) for the backend. See [.github/workflows/ci.yml](.github/workflows/ci.yml).

## License

MIT (or add your own license file).
