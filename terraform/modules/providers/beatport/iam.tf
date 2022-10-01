resource "google_service_account" "beatport" {
  account_id   = "beatport"
  display_name = "Beatport"
  description  = "Beatport ops service account"
}