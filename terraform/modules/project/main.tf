module "naming" {
  source      = "../naming"

  application = var.application
  environment = var.environment
  region      = var.region
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

module "slack" {
  depends_on = [
    google_project_service.apis
  ]

  source      = "../slack"
  application = var.application
  environment = var.environment
  region      = var.region

  function_bucket_name = google_storage_bucket.functions.name
}

module "matching" {
  depends_on = [
    google_project_service.apis
  ]

  source      = "../matching"
  application = var.application
  environment = var.environment
  region      = var.region

  function_bucket_name            = google_storage_bucket.functions.name
  slack_matching_notification_url = module.slack.matching_notification_url
}

locals {
  domain_prefixes = {
    development = "dev-"
    production  = ""
  }
}

module "loadbalancer" {
  depends_on = [
    google_project_service.apis
  ]

  source = "../loadbalancer"

  application = var.application
  environment = var.environment
  redirect_url = var.redirect_url
  region      = var.region

  functions   = {
    domains = [
      "${local.domain_prefixes[var.environment]}functions.${var.domain}"
    ]
    targets = {
      slack = module.slack.function
    }
  } 
}