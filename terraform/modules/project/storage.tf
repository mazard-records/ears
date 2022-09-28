resource "google_storage_bucket" "functions" {
  location = var.cloudstorage_location
  name     = format(module.naming.storage_bucket, "functions")
}