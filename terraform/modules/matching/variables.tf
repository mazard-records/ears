variable "environment" {
  description = "Target environment (development, staging, or production)"
  type        = string
}

variable "producers" {
  default     = ["beatport"]
  description = "List of matching providers"
  type        = list(string)
}
