variable "application" {
  description = "The name for the project"
  type        = string
}

le "environment" {
  description = "Target environment (development, staging, or production)"
  type        = string
}

variable "functions" {
  description = "List of CloudFunction to load balance"
  type        = object({
    domains = list(string)
    targets = map(string)
  })
}

variable "redirect_url" {
  description = "Default URL to redirect when routing fail"
  type        = string
}

variable "region" {
  description = "Default region for resources"
  type        = string
}