resource "google_secret_manager_secret" "deezer" {
  secret_id = format(module.naming.secret, "deezer-access-token")

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "beatport" {
  for_each = toset(["username", "password"])

  secret_id = format(module.naming.secret, "beatport-${each.key}")

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_iam_member" "matching" {
  for_each = toset(var.producers)

  secret_id = google_secret_manager_secret.deezer.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.matching[each.key].email}"
}