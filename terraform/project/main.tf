module "naming" {
  source      = "../naming"
  environment = var.environment
}

provider "google" {
  project = module.naming.project_id
  region  = module.naming.region
}

provider "google-beta" {
  project = module.naming.project_id
  region  = module.naming.region
}

resource "google_project_service" "apis" {
  for_each = toset([
    "cloudbuild",
    "cloudfunctions",
    "iam",
    "pubsub",
    "secretmanager",
    "servicenetworking",
    "storage",
    "vpcaccess",
    "workflows",
  ])

  service            = "${each.key}.googleapis.com"
  disable_on_destroy = false
}

module "matching" {
  depends_on = [
    google_project_service.apis
  ]

  source      = "../matching"
  environment = var.environment

  function_bucket_name = google_storage_bucket.functions.name

  providers = {
    google = google
    google-beta = google-beta
  }
}

module "slack" {
  depends_on = [
    google_project_service.apis
  ]

  source      = "../slack"
  environment = var.environment

  function_bucket_name = google_storage_bucket.functions.name
  matching_topics      = module.matching.topics

  providers = {
    google = google
    google-beta = google-beta
  }
}

locals {
  domain_prefixes = {
    development = "dev."
    production  = ""
  }
}

module "loadbalancer" {
  depends_on = [
    google_project_service.apis
  ]

  source = "../loadbalancer"
  environment = var.environment

  functions   = {
    domains = [
      "${local.domain_prefixes[var.environment]}functions.${var.domain}"
    ]
    targets = {
      slack = module.slack.function
    }
  }

  providers = {
    google = google
    google-beta = google-beta
  }
}