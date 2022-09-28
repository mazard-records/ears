variable "application" {
  default     = "ears"
  description = "The name for the project"
  type        = string
}

variable "cloudstorage_location" {
  default     = "EU"
  description = "GCS storage location"
  type        = string
}

variable "domain" {
  description = "Root DNS entry for services"
  type        = string
}

variable "environment" {
  default     = "development"
  description = "Target environment (development, staging, or production)"
  type        = string
}

variable "redirect_url" {
  description = "URL to redirect unknown request to"
  type        = string
}

variable "region" {
  default     = "europe-west1"
  description = "Default region for resources"
  type        = string
}