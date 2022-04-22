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