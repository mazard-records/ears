locals {
  project = "mzr-ears-production"
  region  = "europe-west1"
}

provider "google" {
  project = local.project
  region  = local.region
}

provider "google-beta" {
  project = local.project
  region  = local.region
}

resource "google_project_service" "apis" {
  for_each = toset([
    "iam",
    "pubsub",
    "secretmanager",
    "storage",
  ])

  service            = "${each.key}.googleapis.com"
  disable_on_destroy = false
}