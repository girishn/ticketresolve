# Guide 2 – S3 bucket for vectors, docs, and tickets.
# Run from this directory: terraform init && terraform plan && terraform apply

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.31"
    }
  }

  # Use local state for learning. For team/production, switch to S3 backend.
  # backend "s3" { ... }
}

provider "aws" {
  region  = var.aws_region
  profile = "ticketresolve"
}

data "aws_caller_identity" "current" {
}

locals {
  bucket_name = "${var.bucket_name_prefix}${data.aws_caller_identity.current.account_id}"
}

resource "aws_s3vectors_vector_bucket" "vectors" {
  vector_bucket_name = local.bucket_name

  encryption_configuration {
    sse_type = "AES256"
  }

  tags = {
    Project = "ticketresolve"
    Guide   = "2_vectors_ingest"
  }
}

# S3 Vectors index for support tickets/documents
resource "aws_s3vectors_index" "support" {
  vector_bucket_name = local.bucket_name
  index_name         = var.index_name

  data_type       = "float32"
  dimension       = var.vector_dimension
  distance_metric = var.distance_metric

  tags = {
    Project = "ticketresolve"
    Guide   = "2_vectors_ingest"
  }
}
