variable "function_bucket" {
  description = "Name of the target function bucket storage"
  type        = string
}

variable "beatport_wantlist" {
  description = "Identifier of the beatport wantlist to use"
  type        = string
}

variable "deezer_wantlist" {
  description = "Identifier of the deezer wantlist to use"
  type        = string
}

variable "publishers" {
  description = "List of service account allowed to publish actions"
  type        = list(string)
}