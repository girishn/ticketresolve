variable "aws_region" {
  description = "AWS region (e.g. ap-southeast-2); used for provider and later for Bedrock/S3"
  type        = string
  default     = "ap-southeast-2"
}

variable "iam_user_name" {
  description = "IAM user name for TicketResolve (e.g. ticketresolve-dev)"
  type        = string
}

variable "iam_policy_name" {
  description = "Name of the IAM policy (e.g. TicketResolveDevPolicy)"
  type        = string
}
