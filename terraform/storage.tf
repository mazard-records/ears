resource "google_storage_bucket" "functions" {
  depends_on = [
    google_project_service.apis
  ]

  location = upper(substr(var.region, 0, 2))
  name     = "functions"
}