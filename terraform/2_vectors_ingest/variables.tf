variable "aws_region" {
  description = "AWS region for the S3 bucket and S3 Vectors index (use same as Bedrock, e.g. ap-southeast-2)"
  type        = string
}

variable "bucket_name_prefix" {
  description = "Globally unique S3 bucket name prefix (must match IAM policy prefix ticketresolve-*, e.g. ticketresolve-vectors-ACCOUNT_ID)"
  type        = string
  default     = "ticketresolve-vectors-"
}

variable "index_name" {
  description = "Name of the S3 Vectors index (e.g. ticketresolve-support-index)"
  type        = string
  default     = "ticketresolve-support-index"
}

variable "vector_dimension" {
  description = "Embedding dimension for the S3 Vectors index (must match the embedding model, e.g. 1024 for Titan v2 text)"
  type        = number
  default     = 1024
}

variable "distance_metric" {
  description = "Distance metric for the S3 Vectors index (cosine or euclidean)"
  type        = string
  default     = "cosine"
}