# Terraform – per-component infrastructure

Each subdirectory is its own Terraform config with its own state. Run Terraform from the directory you care about (e.g. `terraform/2_vectors_ingest/`).

| Directory            | What it does |
|----------------------|---------------|
| `1_permissions/`     | IAM user and policy for TicketResolve (Guide 1, Step 2). |
| `2_vectors_ingest/` | S3 bucket for vectors, docs, and tickets (Guide 2). |

Before you apply, copy `terraform.tfvars.example` to `terraform.tfvars` in that directory and set your values. Don’t commit `terraform.tfvars`.
