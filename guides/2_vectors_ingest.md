# Guide 2 – Vectors and ingest

This guide is about how we store RAG data, how chunking and embedding fit in, and why we use S3 (and S3 Vectors) for this project. Finish Guide 1 first, then go through this one step by step.

---

## What we’re doing here

1. **Create the S3 Vectors bucket and index with Terraform** — one S3 bucket and one S3 Vectors index for vectors, raw docs, and tickets.
2. **Define the bucket layout** — prefixes for `docs/raw`, `docs/chunks`, and `tickets/`.
3. **Add an ingest script/Lambda later** — chunk docs/tickets, call Bedrock for embeddings, write vectors into the S3 Vectors index.

This guide focuses on **Step 1 (Terraform)** so the bucket and S3 Vectors index exist and are managed as code. The ingest pipeline comes in a follow-up step or day.

---

## Step 1 – Create the S3 Vectors bucket and index with Terraform

**1.1 – Go to the Terraform directory**

```bash
cd terraform/2_vectors_ingest
```

**1.2 – Set your variables**

Copy the example and fill in your values (same region as Guide 1; bucket name must be globally unique and match the IAM prefix `ticketresolve-*`):

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

- `aws_region` – e.g. `ap-southeast-2`
- `bucket_name_prefix` – usually keep the default `ticketresolve-vectors-` so the bucket becomes `ticketresolve-vectors-<account_id>`
- `index_name` – e.g. `ticketresolve-support-index`
- `vector_dimension` – must match your embedding model (e.g. `1024` for Titan v2 text; we start with 1024)
- `distance_metric` – usually `cosine` for text embeddings

**1.3 – Init and apply**

```bash
terraform init
terraform plan
terraform apply
```

Type `yes` when prompted. You should see outputs for `bucket_name`, `bucket_arn`, `vector_index_name`, and `vector_index_arn`.

**1.4 – Quick check**

```bash
aws s3 ls s3://YOUR_BUCKET_NAME
```

The bucket will be empty for now; we’ll add the object layout and ingest in the next steps. The S3 Vectors index is created in that bucket and is ready for vectors.

Terraform keeps the bucket and index in code (versioned, encrypted, no public access). To change them later, edit the `.tf` files and run `terraform apply` again. Note that index dimension and metric are immutable — to change those you’d create a new index.

---

## Step 2 – Bucket layout (for later ingest)

We use one bucket with these prefixes:

| Prefix        | Purpose |
|---------------|--------|
| `docs/raw/`   | Original documents (e.g. PDF, Markdown) before chunking. |
| `docs/chunks/`| Chunked text + metadata (and later embeddings) for RAG. |
| `tickets/`    | Sample historical tickets and resolutions for similarity search. |

No Terraform changes are needed for these; the ingest script (when we add it) will write under these prefixes.

---

## Step 3 – What comes next (ingest pipeline)

In a follow-up step we’ll add:

- A script or Lambda that reads from `docs/raw/` and `tickets/`, chunks the text, calls Bedrock (or SageMaker) for embeddings, and writes to `docs/chunks/` (and uses S3 Vectors APIs when we wire up search).
- Dependencies in `backend/ingest/` and any CI wiring.

For now you have a Terraform-managed S3 bucket and index ready for that ingest work and for Guide 3.

---

## Checklist

- [ ] `terraform/2_vectors_ingest/terraform.tfvars` created (and not committed).
- [ ] `terraform init`, `terraform plan`, and `terraform apply` ran successfully.
- [ ] Bucket exists and shows up with `aws s3 ls`.
- [ ] You know the bucket name and region for the ingest script and Guide 3.

When you’re ready, you can continue with the ingest script (chunking + embeddings) or move on to **Guide 3 – Agents** and use this bucket from the resolver tools.
