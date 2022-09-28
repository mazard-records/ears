variable "environment" {
  description = "Target environment (development, staging, or production)"
  type        = string
}

variable "function_bucket_name" {
  description = "Name of the target function bucket storage"
  type        = string
}

variable "matching_topics" {
  description = "List of PubSub matching topic name to listen to"
  type        = list(string)
}