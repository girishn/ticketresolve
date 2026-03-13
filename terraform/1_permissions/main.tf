# Guide 1, Step 2 – IAM user and policy for TicketResolve (least-privilege).
# Run from this directory: terraform init && terraform plan && terraform apply

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.31"
    }
  }
}

provider "aws" {
  region = var.aws_region
  profile = "default"
}

resource "aws_iam_user" "dev" {
  name = var.iam_user_name
  path = "/"

  tags = {
    Project = "ticketresolve"
    Guide   = "1_permissions"
  }
}

resource "aws_iam_policy" "dev" {
  name        = var.iam_policy_name
  description = "Least-privilege policy for TicketResolve (Bedrock + S3 ticketresolve-* buckets)"
  path        = "/"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "BedrockInvoke"
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = "*"
      },
      {
        Sid    = "STSGetCallerIdentity"
        Effect = "Allow"
        Action = [
          "sts:GetCallerIdentity"
        ]
        Resource = "*"
      },
      {
        Sid    = "S3TicketResolveBuckets"
        Effect = "Allow"
        Action = [
          "s3:*"
        ]
        Resource = [
          "arn:aws:s3:::ticketresolve-*",
          "arn:aws:s3:::ticketresolve-*/*"
        ]
      },
      {
        Sid    = "S3VectorsManagement"
        Effect = "Allow"
        Action = [
          "s3vectors:*"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_user_policy_attachment" "dev" {
  user       = aws_iam_user.dev.name
  policy_arn = aws_iam_policy.dev.arn
}
