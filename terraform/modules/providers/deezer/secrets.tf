resource "google_secret_manager_secret" "deezer" {
  secret_id = "deezer-access-token"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_iam_member" "deezer" {
  for_each = toset(var.producers)

  secret_id = google_secret_manager_secret.deezer.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.matching[each.key].email}"
}