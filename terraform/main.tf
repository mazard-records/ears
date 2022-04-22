terraform {
  backend "gcs" {
    bucket  = "mzr-ears-p-gcs-tfstate"
    prefix  = "ears"
  }
}

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