variable "application" {
  description = "The name for the project"
  type        = string
}

variable "cloudstorage_location" {
  description = "GCS storage location"
  type        = string
}

variable "domain" {
  description = "Root DNS entry for services"
  type        = string
}

variable "environment" {
  description = "Target environment (development, staging, or production)"
  type        = string
}

variable "redirect_url" {
  description = "URL to redirect unknown request to"
  type        = string
}

variable "region" {
  description = "Default region for resources"
  type        = string
}

variable "beatport_wantlist" {
  description = "Identifier of the beatport wantlist to use"
  type        = string
}