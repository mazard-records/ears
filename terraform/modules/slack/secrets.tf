resource "google_secret_manager_secret" "slack" {
  for_each = toset([
    "signing_key",
    "webhook",
  ])

  secret_id = format(module.naming.secret, "slack-${each.key}")

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_iam_member" "slack" {
  for_each = google_secret_manager_secret.slack

  secret_id = each.value.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.slack.email}"
}