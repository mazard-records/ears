provider "google" {
  project = var.project
  region  = var.region
}

provider "google-beta" {
  project = var.project
  region  = var.project
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
    module.matching.beatport_service_account,
    module.matching.deezer_service_account,
    module.slack.service_account,
  ]
}