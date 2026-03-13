output "iam_user_name" {
  description = "Name of the IAM user for TicketResolve"
  value       = aws_iam_user.dev.name
}

output "iam_user_arn" {
  description = "ARN of the IAM user"
  value       = aws_iam_user.dev.arn
}

output "iam_policy_arn" {
  description = "ARN of the TicketResolve dev policy"
  value       = aws_iam_policy.dev.arn
}

output "next_step" {
  description = "Create access keys in IAM Console for this user, then run: aws configure"
  value       = "IAM → Users → ${aws_iam_user.dev.name} → Security credentials → Create access key"
}
