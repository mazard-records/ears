resource "google_secret_manager_secret" "beatport_username" {
  secret_id = "beatport-username"

  replication {
    automatic = true
  }
}
resource "google_secret_manager_secret" "beatport_password" {
  secret_id = "beatport-password"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "deezer_access_token" {
  secret_id = "deezer-access-token"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_iam_member" "beatport_username" {
  secret_id = google_secret_manager_secret.beatport_username.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.beatport.email}"
}

resource "google_secret_manager_secret_iam_member" "beatport_password" {
  secret_id = google_secret_manager_secret.beatport_password.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.beatport.email}"
}

resource "google_secret_manager_secret_iam_member" "deezer_access_token" {
  secret_id = google_secret_manager_secret.deezer_access_token.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.deezer.email}"
}