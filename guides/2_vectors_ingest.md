# Guide 2 – Vectors and ingest

**Learning outcome:** Understand how RAG data is stored, how chunking and embedding work, and why we use S3 (and optionally S3 Vectors) for this project.

Complete Guide 1 first. Work through this guide step-by-step.

---

## What you’ll do

1. **Create the S3 Vectors bucket and index with Terraform** – one S3 bucket and one S3 Vectors index for vectors, raw docs, and tickets.
2. **Define the bucket layout** – prefixes for `docs/raw`, `docs/chunks`, `tickets/`.
3. **Add an ingest script/Lambda** (in a later step or day) – chunk docs/tickets, call Bedrock for embeddings, write vectors into the S3 Vectors index.

This guide focuses on **Step 1 (Terraform)** so the bucket and S3 Vectors index exist and are managed as code.

---

## Step 1 – Create the S3 Vectors bucket and index with Terraform

**1.1 – Go to the Terraform directory**

```bash
cd terraform/2_vectors_ingest
```

**1.2 – Create your variables file**

Copy the example and set your values (use the same region as in Guide 1; bucket name must be globally unique and match the IAM prefix `ticketresolve-*`):

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

- `aws_region` – e.g. `ap-southeast-2`
- `bucket_name_prefix` – usually leave as the default `ticketresolve-vectors-` so the bucket name becomes `ticketresolve-vectors-<account_id>`.
- `index_name` – e.g. `ticketresolve-support-index`.
- `vector_dimension` – must match your embedding model (e.g. `1024` for Titan v2 text; we start with 1024).
- `distance_metric` – usually `cosine` for text embeddings.

**1.3 – Initialize and apply**

```bash
terraform init
terraform plan
terraform apply
```

Type `yes` when prompted. You should see outputs: `bucket_name`, `bucket_arn`, `vector_index_name`, and `vector_index_arn`.

**1.4 – Verify**

```bash
aws s3 ls s3://YOUR_BUCKET_NAME
```

The bucket is empty; we’ll add object layout and ingest in the next steps. The S3 Vectors index is created in that bucket and is ready to accept vectors.

**Learning note:** Terraform keeps the bucket and index definitions in code (versioned, encrypted, no public access). Changing them later is done by editing `.tf` files and re-running `terraform apply` (note that index dimension/metric are immutable; to change them you’d create a new index).

---

## Step 2 – Bucket layout (for later ingest)

We’ll use a single bucket with prefixes:

| Prefix        | Purpose |
|---------------|--------|
| `docs/raw/`   | Original documents (e.g. PDF, Markdown) before chunking. |
| `docs/chunks/`| Chunked text + metadata (and later embeddings) for RAG. |
| `tickets/`    | Sample historical tickets and resolutions for similarity search. |

No Terraform changes are required for these; the ingest script (Guide 2 continued or a separate day) will write objects under these prefixes.

---

## Step 3 – (Next) Ingest pipeline

In a follow-up step we’ll add:

- A script or Lambda that reads from `docs/raw/` and `tickets/`, chunks text, calls Bedrock (or SageMaker) for embeddings, and writes to `docs/chunks/` (and optionally uses S3 Vectors APIs when we integrate search).
- Dependencies in `backend/ingest/` and wiring into CI if needed.

For now, you have a Terraform-managed S3 bucket ready for Guide 2’s ingest work.

---

## Checklist

- [ ] `terraform/2_vectors_ingest/terraform.tfvars` created (not committed).
- [ ] `terraform init`, `terraform plan`, `terraform apply` run successfully.
- [ ] Bucket exists and is listed with `aws s3 ls`.
- [ ] You know the bucket name and region for use in the ingest script and Guide 3.

When ready, continue with the ingest script (chunking + embeddings) or move to **Guide 3 – Agents** and use this bucket for resolver tools.
