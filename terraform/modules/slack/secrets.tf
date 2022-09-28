resource "google_secret_manager_secret" "slack_webhook" {
  secret_id = format(module.naming.secret, "slack-webhook")

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_iam_member" "slack_webhook" {
  secret_id = google_secret_manager_secret.slack_webhook.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.slack.email}"
}