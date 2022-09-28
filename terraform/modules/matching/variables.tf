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
