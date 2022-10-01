variable "name" {
  description = "Function name"
  type        = string
}

variable "path" {
  description = "Function source path relative to root functions directory"
  type        = string
}

variable "description" {
  description = "Function description"
  type        = string
}

variable "entrypoint" {
  description = "Function entrypoint"
  type        = string
}

variable "service_account" {
  description = "Function service account"
  type        = string
}

variable "bucket" {
  description = "Target bucket for sources storage"
  type        = string
}

variable "memory" {
  default     = 128
  description = "Function allocated memory"
  type        = number
}

variable "envvars" {
  default     = {}
  description = "Function environment variables"
  type        = map 
}

variable "secrets" {
  default     = {}
  description = "Function secret environment variable as KEY = secret_id"
  type        = map
}

variable "ingress" {
  default     = "ALLOW_INTERNAL_ONLY"
  description = "Function ingress policy"
  type        = string
}

variable "invokers" {
  default     = []
  description = "Service account to provide invoker role"
  type        = list(string)
}

variable "all_users" {
  default     = false
  description = "Indicate if function unauthorized access is allowed"
  type        = bool
}