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
    "iam",
    "pubsub",
    "secretmanager",
    "servicenetworking",
    "storage",
    "vpcaccess",
  ])

  service            = "${each.key}.googleapis.com"
  disable_on_destroy = false
}

module "matching" {
  source      = "../matching"
  environment = var.environment

  function_bucket_name = google_storage_bucket.functions.name
}

module "slack" {
  source      = "../slack"
  environment = var.environment

  function_bucket_name = google_storage_bucket.functions.name
  matching_topics      = module.matching.topics
}

locals {
  domain_prefixes = {
    development = "dev."
    production  = ""
  }
}

module "loadbalancer" {
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
}