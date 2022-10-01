resource "google_secret_manager_secret" "signing_key" {
  secret_id = "slack-signing-key"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "webhook" {
  secret_id = "slack-webhook"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_iam_member" "signing_key" {
  secret_id = google_secret_manager_secret.signing_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.slack.email}"
}

resource "google_secret_manager_secret_iam_member" "webhook" {
  secret_id = google_secret_manager_secret.webhook.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.slack.email}"
}