resource "google_secret_manager_secret" "beatport" {
  for_each = toset(["username", "password"])

  secret_id = "beatport-${each.key}"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_iam_member" "beatport" {
  for_each = toset(["username", "password"])

  secret_id = google_secret_manager_secret.beatport[each.key].secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.beatport.email}"
}