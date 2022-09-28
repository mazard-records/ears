variable "functions" {
  description = "List of CloudFunction to load balance"
  type        = object({
    domains = list(string)
    targets = map(string)
  })
}

variable "environment" {
  description = "Target environment (development, staging, or production)"
  type        = string
}

variable "redirect_url" {
  default     = "www.mazard-records.fr"
  description = "Default URL to redirect when routing fail"
  type        = string
}