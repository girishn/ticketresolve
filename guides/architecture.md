# TicketResolve – Architecture

This page is the high-level picture. We update it as we add components in each guide so it stays in sync with the repo.

## Where we are now

- **Repo:** TicketResolve on GitHub with CI (lint + test).
- **Guide 1:** Permissions and AWS setup (in progress or done, depending on where you are).

## Where we’re headed (from the gameplan)

- **API:** FastAPI in `backend/api/` — tickets CRUD, `POST /tickets/{id}/resolve`, `GET /tickets/{id}/agent-trace`.
- **Agent:** Single resolver in `backend/resolver/` — orchestration, tools (knowledge search, ticket history, policy checker), draft, then policy check.
- **Data:** S3 for raw docs, S3 Vectors for chunks/embeddings, and sample tickets.
- **AWS:** Bedrock (chat + optional embeddings), S3 Vectors, Lambda and/or App Runner, API Gateway, Terraform per component.

For directory layout and the agent flow diagram, see [gameplan.md](../gameplan.md).
