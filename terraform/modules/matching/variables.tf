variable "consumers" {
  description = "List of matching consumer service account email"
  type        = list(string)
}

variable "providers" {
  default     = ["beatport"]
  description = "List of matching providers"
  type        = list(string)
}
