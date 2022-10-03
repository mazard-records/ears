terraform {
  cloud {
    organization = "mazard-records"

    workspaces {
      name = "ears"
    }
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.38.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "4.38.0"
    }
    tfe = {
      version = "~> 0.37.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

provider "google-beta" {
  project = var.project
  region  = var.project
}
