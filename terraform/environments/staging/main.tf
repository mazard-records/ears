terraform {
  cloud {
    organization = "mazard-records"

    workspaces {
      name = "ears-staging"
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

module "ears_staging" {
  source = "../../modules/ears"

  project           = var.project
  region            = var.region
  beatport_wantlist = var.beatport_wantlist
  deezer_wantlist   = var.deezer_wantlist
}