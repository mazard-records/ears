variable "application" {
  description = "The name for the project"
  type        = string
}

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

variable "region" {
  description = "Default region for resources"
  type        = string
}