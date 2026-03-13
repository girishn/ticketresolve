output "bucket_name" {
  description = "Name of the S3 bucket for vectors, docs, and tickets"
  value       = aws_s3vectors_vector_bucket.vectors.vector_bucket_name
}

output "bucket_arn" {
  description = "ARN of the S3 vector bucket"
  value       = aws_s3vectors_vector_bucket.vectors.vector_bucket_arn
}

output "vector_index_name" {
  description = "Name of the S3 Vectors index"
  value       = aws_s3vectors_index.support.index_name
}

output "vector_index_arn" {
  description = "ARN of the S3 Vectors index"
  value       = aws_s3vectors_index.support.index_arn
}
