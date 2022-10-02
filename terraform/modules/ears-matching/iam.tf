resource "google_service_account" "beatport" {
  account_id   = "beatport"
  display_name = "Beatport"
  description  = "Beatport ops service account"
}

resource "google_service_account" "deezer" {
  account_id   = "deezer"
  display_name = "Deezer"
  description  = "Deezer ops service account"
}