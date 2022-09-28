variable "region" {
  description = "Target region to deploy resources into"
  type        = string
}

variable "environment" {
  description = "The environment of the project"
  type        = string
}

variable "application" {
  description = "The name for the project"
  type        = string
}