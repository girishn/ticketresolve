# Terraform – per-component infrastructure

Each subdirectory is a separate Terraform configuration with its own state. Run commands from the specific directory (e.g. `terraform/2_vectors_ingest/`).

| Directory            | Purpose |
|----------------------|--------|
| `1_permissions/`     | IAM user and policy for TicketResolve (Guide 1, Step 2). |
| `2_vectors_ingest/` | S3 bucket for vectors, docs, and tickets (Guide 2). |

Before applying, copy `terraform.tfvars.example` to `terraform.tfvars` in that directory and set your values. Do not commit `terraform.tfvars`.
