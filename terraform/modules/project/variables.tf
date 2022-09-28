variable "cloudstorage_location" {
  default     = "EU"
  description = "GCS storage location"
  type        = string
}

variable "domain" {
  default     = "mazard-records.fr"
  description = "Root DNS entry for services"
  type        = string
}

variable "environment" {
  description = "Target environment (development, staging, or production)"
  type        = string
}