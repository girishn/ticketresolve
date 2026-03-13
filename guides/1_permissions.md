# Guide 1 – Permissions and AWS setup

**Learning outcome:** Understand why we use least-privilege IAM, how Bedrock and S3 are accessed, and how to configure your local AWS environment for TicketResolve.

Work through this guide in one or two sessions. Do not skip steps.

---

## What you’ll do

1. Create a GitHub repo and push this project (if not already done).
2. Create an IAM user (or use an existing one) with only the permissions TicketResolve needs.
3. Enable Bedrock model access in your AWS account.
4. Configure the AWS CLI locally and verify access to Bedrock and S3.

---

## Step 1 – Put the project on GitHub

If the project is not on GitHub yet:

1. **Create a new repository** on GitHub (e.g. `ticketresolve`). Do not add a README, .gitignore, or license (we already have them).

2. **Initialize git and push** (from the project root):

   ```bash
   git init
   git add .
   git commit -m "Initial commit: gameplan, README, CI, backend skeleton, Guide 1"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ticketresolve.git
   git push -u origin main
   ```

3. **Confirm CI runs:** Open the repo on GitHub → Actions. You should see a run for the push; the “lint-and-test” job should pass.

**Why:** Having the project on GitHub with CI gives you a single place to push changes and see that lint and tests pass before moving to the next guide.

---

## Step 2 – IAM user and least-privilege

We use a dedicated IAM user (or role) for TicketResolve so that:

- Permissions are limited to what the project needs (Bedrock, S3).
- You can revoke or rotate access without affecting other work.

**2.1 – Create an IAM user (or reuse one)**

1. In the AWS Console go to **IAM** → **Users** → **Create user**.
2. User name: e.g. `ticketresolve-dev`.
3. Do **not** add the user to any group yet; we’ll attach a custom policy in the next step.

**2.2 – Create a policy for TicketResolve**

1. Go to **IAM** → **Policies** → **Create policy**.
2. Choose **JSON** and use the policy below. Replace `YOUR_ACCOUNT_ID` and `ticketresolve-*` with your account ID and a bucket name prefix you’ll use (e.g. `ticketresolve-vectors-dev`).

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "BedrockInvoke",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "*"
    },
    {
      "Sid": "S3TicketResolveBuckets",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::ticketresolve-*",
        "arn:aws:s3:::ticketresolve-*/*"
      ]
    }
  ]
}
```

3. Name the policy e.g. `TicketResolveDevPolicy` and create it.

**2.3 – Attach the policy to the user**

1. Go back to **IAM** → **Users** → `ticketresolve-dev`.
2. **Add permissions** → **Attach policies directly** → select `TicketResolveDevPolicy` → Add permissions.

**Learning note:** We only grant `InvokeModel` (and stream) for Bedrock and object/bucket operations for S3 buckets whose names start with `ticketresolve-*`. This is least-privilege: no EC2, Lambda, or other services.

---

## Step 3 – Enable Bedrock model access

Bedrock requires you to enable each model in the console before your code can call it.

1. In the AWS Console switch to a region where Bedrock is available (e.g. **us-east-1** or **us-west-2**).
2. Open **Amazon Bedrock** → **Model access** (or **Get started** → **Manage model access**).
3. **Enable** at least one model you’ll use for TicketResolve, for example:
   - **Claude 3.5 Sonnet** or **Claude 3 Haiku** (Anthropic), or  
   - **Amazon Nova Lite** or **Nova Pro** (Amazon).

You can enable more later. For Guide 3 we’ll need at least one chat model; for embeddings (Guide 2) we’ll use Bedrock Titan or Cohere if you enable them.

---

## Step 4 – Configure AWS CLI and verify

**4.1 – Configure the CLI**

On your machine, configure the CLI to use the IAM user you created:

```bash
aws configure
```

- **AWS Access Key ID** / **Secret Access Key**: create access keys for `ticketresolve-dev` in IAM → Users → Security credentials → Create access key (e.g. “Command line use”).
- **Default region**: e.g. `us-east-1` (must be a region where Bedrock is available).
- **Output format**: `json` is fine.

**4.2 – Verify Bedrock access**

List available foundation models (optional; confirms Bedrock API is reachable):

```bash
aws bedrock list-foundation-models --region us-east-1 --query "modelSummaries[?contains(modelId, 'claude') || contains(modelId, 'nova')].[modelId]" --output table
```

Or invoke a model (replace `MODEL_ID` with an enabled model, e.g. `anthropic.claude-3-5-sonnet-20241022-v2:0` in us-east-1):

```bash
aws bedrock-runtime invoke-model --region us-east-1 --model-id MODEL_ID --body "{\"anthropic_version\":\"bedrock-2023-05-31\",\"max_tokens\":50,\"messages\":[{\"role\":\"user\",\"content\":\"Say hello in one word.\"}]}" --content-type application/json out.json
```

Then open `out.json` to confirm you get a response (you’ll see content in the file).

**4.3 – Verify S3 access**

Create a test bucket (use a globally unique name):

```bash
aws s3 mb s3://ticketresolve-vectors-YOUR_ACCOUNT_ID --region us-east-1
aws s3 ls s3://ticketresolve-vectors-YOUR_ACCOUNT_ID
```

Then delete it if you like (we’ll create the real bucket in Guide 2):

```bash
aws s3 rb s3://ticketresolve-vectors-YOUR_ACCOUNT_ID
```

If both Bedrock and S3 commands succeed, your permissions and CLI setup are correct.

---

## Step 5 – Document your choices (optional but useful)

In your notes or a local file (do **not** commit secrets), record:

- IAM user name and policy name.
- AWS region you’re using (e.g. `us-east-1`).
- Bedrock model ID you enabled (e.g. `anthropic.claude-3-5-sonnet-20241022-v2:0`).
- S3 bucket name prefix you’ll use (e.g. `ticketresolve-vectors-`).

You’ll need these in Guide 2 and 3.

---

## Checklist

- [ ] Repo is on GitHub and CI (lint + test) passes.
- [ ] IAM user created with a policy that allows only Bedrock invoke and S3 for `ticketresolve-*` buckets.
- [ ] At least one Bedrock model enabled in your chosen region.
- [ ] `aws configure` done with that user’s keys and the correct region.
- [ ] Bedrock and S3 commands run successfully from the CLI.

When all are done, you’re ready for **Guide 2 – Vectors and ingest** (S3 Vectors bucket and document/ticket ingestion pipeline).
