variable "project" {
  description = "Target GCP project to apply this configuration for"
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