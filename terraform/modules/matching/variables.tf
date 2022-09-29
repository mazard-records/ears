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

variable "producers" {
  default     = ["beatport"]
  description = "List of matching providers"
  type        = list(string)
}

variable "region" {
  description = "Default region for resources"
  type        = string
}

variable "slack_matching_notification_name" {
  description = "Function to send notification to"
  type        = string
}

variable "slack_matching_notification_url" {
  description = "URL to send notification to"
  type        = string
}