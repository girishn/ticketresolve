# TicketResolve – Architecture

High-level architecture. Update this as we add components in each guide.

## Current state

- **Repo**: TicketResolve on GitHub with CI (lint + test).
- **Guide 1**: Permissions and AWS setup (in progress).

## Target architecture (from gameplan)

- **API**: FastAPI in `backend/api/` — tickets CRUD, `POST /tickets/{id}/resolve`, `GET /tickets/{id}/agent-trace`.
- **Agent**: Single resolver in `backend/resolver/` — orchestration, tools (knowledge search, ticket history, policy checker), draft, policy check.
- **Data**: S3 (raw docs, S3 Vectors for chunks/embeddings, sample tickets).
- **AWS**: Bedrock (chat + optional embeddings), S3 Vectors, Lambda and/or App Runner, API Gateway, Terraform per component.

See [gameplan.md](../gameplan.md) for the directory structure and agent flow diagram.
