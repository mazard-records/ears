provider "google" {
  project = var.project
  region  = var.region
}

provider "google-beta" {
  project = var.project
  region  = var.project
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

resource "google_storage_bucket" "functions" {
  depends_on = [
    google_project_service.apis
  ]

  location = upper(substr(var.region, 0, 2))
  name     = "functions"
}

module "slack" {
  depends_on = [google_storage_bucket.functions]
  source     = "../ears-slack"

  function_bucket = google_storage_bucket.functions.name
}

module "matching" {
  depends_on = [google_storage_bucket.functions]
  source     = "../ears-matching"

  function_bucket   = google_storage_bucket.functions.name
  beatport_wantlist = var.beatport_wantlist
  deezer_wantlist   = var.deezer_wantlist
  publishers        = [module.slack.service_account]
}

module "cloudlogging" {
  source = "../cloudlogging"

  project = var.project
  writers = [
    module.beatport.service_account,
    module.slack.service_account,
  ]
}