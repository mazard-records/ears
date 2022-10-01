module "search_notification" {
  source = "../../cloudfunction/https"

  path   = "slack"
  bucket = var.function_bucket

  name            = "slack-search-notification"
  description     = "Slack bot that produces interactive matching notification"
  entrypoint      = "on_matching_event"
  service_account = google_service_account.slack.email

  secrets = {
    SLACK_SIGNING_KEY = google_secret_manager_secret.signing_secret.secret_id
    SLACK_WEBHOOK = google_secret_manager_secret.webhook.secret_id
  }
}

module "interactivity_webhook" {
  source = "../../cloudfunction/https"

  path   = "slack"
  bucket = var.function_bucket

  name            = "slack-interactivity-webhook"
  description     = "Slack webhook for receiving interactive user feedback"
  entrypoint      = "on_interactive_webhook"
  ingress         = "ALLOW_ALL"
  service_account = google_service_account.slack.email
  all_users       = true

  secrets = {
    SLACK_SIGNING_KEY = google_secret_manager_secret.signing_secret.secret_id
    SLACK_WEBHOOK = google_secret_manager_secret.webhook.secret_id
  }

}