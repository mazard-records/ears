resource "google_service_account" "publisher" {
  account_id   = "publisher"
  display_name = "Publisher"
  description  = "Service account for pub/sub message push"
}

resource "google_service_account" "beatport" {
  account_id   = "beatport"
  display_name = "Beatport"
  description  = "Service account for Beatport related ops"
}