# Guide 1 – Permissions and AWS setup

By the end of this guide you’ll understand why we use least-privilege IAM, how we talk to Bedrock and S3, and how to configure your local AWS environment for TicketResolve. Plan for one or two sessions and go through the steps in order — skipping ahead tends to cause confusion later.

---

## Step 1 – Put the project on GitHub

If it’s not there already:

1. **Create a new repo** on GitHub (e.g. `ticketresolve`). Don’t add a README, .gitignore, or license — we already have those.

2. **Init and push** from the project root:

   ```bash
   git init
   git add .
   git commit -m "Initial commit: gameplan, README, CI, backend skeleton, Guide 1"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ticketresolve.git
   git push -u origin main
   ```

3. **Check that CI runs:** On GitHub, open the repo → Actions. You should see a run from the push; the “lint-and-test” job should be green.

Having the project on GitHub with CI gives you a single place to push and confirm that lint and tests pass before you move on.

---

## Step 2 – IAM user and least-privilege (Terraform)

We use a dedicated IAM user for TicketResolve so that:

- Permissions are limited to what this project actually needs (Bedrock and S3).
- You can revoke or rotate access without touching other work.
- Everything is in code (Terraform), so it’s repeatable and easy to review.

**2.1 – Create the IAM user and policy with Terraform**

1. Go to the Terraform directory:

   ```bash
   cd terraform/1_permissions
   ```

2. Copy the example variables and fill in your values:

   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

   Edit `terraform.tfvars`: set `aws_region` (e.g. `ap-southeast-2`), `iam_user_name` (e.g. `ticketresolve-dev`), and `iam_policy_name` (e.g. `TicketResolveDevPolicy`).

3. Init and apply:

   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

   Type `yes` when prompted. Terraform creates the IAM user, a policy that allows Bedrock invoke and S3 only for `ticketresolve-*` buckets, and attaches that policy to the user.

4. Note the output `next_step`: you’ll create access keys for this user in the console in Step 4.1.

The policy only grants `InvokeModel` (and stream) for Bedrock and object/bucket operations for S3 buckets whose names start with `ticketresolve-*`. No EC2, Lambda, or other services — that’s least-privilege. The Terraform lives in `terraform/1_permissions/` so you can tweak or re-apply it later.

---

## Step 3 – Enable Bedrock model access

Bedrock makes you enable each model in the console before your code can call it.

1. In the AWS Console, pick a region where Bedrock is available (e.g. **ap-southeast-2** or **us-west-2**).
2. Open **Amazon Bedrock** → **Model access** (or **Get started** → **Manage model access**).
3. **Enable** at least one model you’ll use for TicketResolve, e.g.:
   - **Claude 3.5 Sonnet** or **Claude 3 Haiku** (Anthropic), or
   - **Amazon Nova Lite** or **Nova Pro** (Amazon).

You can enable more later. For Guide 3 we need at least one chat model; for embeddings (Guide 2) we’ll use Bedrock Titan or Cohere if you enable them.

---

## Step 4 – Configure AWS CLI and verify

**4.1 – Configure the CLI**

On your machine, point the CLI at the IAM user you created:

```bash
aws configure
```

- **AWS Access Key ID** / **Secret Access Key**: Create access keys for `ticketresolve-dev` in IAM → Users → Security credentials → Create access key (e.g. “Command line use”).
- **Default region**: e.g. `ap-southeast-2` (must be a region where Bedrock is available).
- **Output format**: `json` is fine.

**4.2 – Verify Bedrock**

List available foundation models (optional; confirms the Bedrock API is reachable):

```bash
aws bedrock list-foundation-models --region ap-southeast-2 --query "modelSummaries[?contains(modelId, 'claude') || contains(modelId, 'nova')].[modelId]" --output table
```

Or invoke a model (replace `MODEL_ID` with an enabled model, e.g. `anthropic.claude-3-5-sonnet-20241022-v2:0` in ap-southeast-2):

```bash
aws bedrock-runtime invoke-model --region ap-southeast-2 --model-id MODEL_ID --body "{\"anthropic_version\":\"bedrock-2023-05-31\",\"max_tokens\":50,\"messages\":[{\"role\":\"user\",\"content\":\"Say hello in one word.\"}]}" --content-type application/json out.json
```

Open `out.json` to confirm you get a response.

**4.3 – Verify S3**

Create a test bucket (use a globally unique name):

```bash
aws s3 mb s3://ticketresolve-vectors-YOUR_ACCOUNT_ID --region ap-southeast-2
aws s3 ls s3://ticketresolve-vectors-YOUR_ACCOUNT_ID
```

You can delete it afterward (we’ll create the real bucket in Guide 2):

```bash
aws s3 rb s3://ticketresolve-vectors-YOUR_ACCOUNT_ID
```

If both Bedrock and S3 commands work, your permissions and CLI setup are good.

---

## Step 5 – Write down your choices (optional but helpful)

In your notes or a local file (don’t commit secrets), record:

- IAM user name and policy name
- AWS region (e.g. `ap-southeast-2`)
- Bedrock model ID you enabled (e.g. `anthropic.claude-3-5-sonnet-20241022-v2:0`)
- S3 bucket name prefix (e.g. `ticketresolve-vectors-`)

You’ll need these in Guide 2 and 3.

---

## Checklist

- [ ] Repo is on GitHub and CI (lint + test) passes.
- [ ] IAM user created with a policy that allows only Bedrock invoke and S3 for `ticketresolve-*` buckets.
- [ ] At least one Bedrock model enabled in your chosen region.
- [ ] `aws configure` done with that user’s keys and the correct region.
- [ ] Bedrock and S3 commands run successfully from the CLI.

When all of that is done, you’re ready for **Guide 2 – Vectors and ingest** (S3 Vectors bucket and the doc/ticket ingestion pipeline).
