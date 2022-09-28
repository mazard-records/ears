resource "google_service_account" "slack" {
  account_id   = "slackbot"
  display_name = "Slack bot"
  description  = "Slack bot service account"
}