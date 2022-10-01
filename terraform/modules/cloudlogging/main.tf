variable "project" {
  description = "Target GCP project to set IAM for"
  type        = string
}

variable "writers" {
  description = "List of service account with logWriter role"
  type        = list(string)
}

resource "google_project_iam_binding" "logging" {
  for_each = toset(var.writers)

  project = var.project
  role    = "roles/logging.logWriter"
  members = [
    "serviceAccount:${each.key}"
  ]
}