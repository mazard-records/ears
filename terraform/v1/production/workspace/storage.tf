resource "google_storage_bucket" "functions" {
  location = local.region
  name     = "mzr-ears-p-gcs-functions"

  force_destroy = true
}
