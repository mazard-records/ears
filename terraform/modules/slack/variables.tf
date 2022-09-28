variable "environment" {
  description = "Target environment (development, staging, or production)"
  type        = string
}

variable "matching_topics" {
  description = "List of PubSub matching topic name to listen to"
  type        = list(string)
}