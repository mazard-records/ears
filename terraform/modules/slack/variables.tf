variable "environment" {
  description = "Target environment (development, staging, or production)"
  type        = string
}

variable "matching_topic" {
  description = "PubSub matching topic name to listen to"
  type        = string
}