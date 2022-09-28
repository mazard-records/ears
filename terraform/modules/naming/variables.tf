variable "region" {
  description = "Target region to deploy resources into"
  type        = string
  default     = "europe-west1"
}

variable "environment" {
  description = "The environment of the project"
  type        = string
}

variable "application" {
  default     = "ears"
  description = "The name for the project"
  type        = string
}