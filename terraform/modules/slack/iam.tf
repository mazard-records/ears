resource "google_service_account" "slack" {
  account_id   = "slack"
  display_name = "Slack"
  description  = "Slack bot service account"
}