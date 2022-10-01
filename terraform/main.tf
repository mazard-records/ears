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
  source     = "../slack"

  function_bucket = google_storage_bucket.functions.name
}

module "deezer" {
  depends_on = [google_storage_bucket.functions]
  source     = "../providers/deezer"
}

module "beatport" {
  depends_on = [google_storage_bucket.functions]
  source     = "../providers/beatport"

  function_bucket   = google_storage_bucket.functions.name
  beatport_wantlist = var.beatport_wantlist
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