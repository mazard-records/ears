resource "google_service_account" "beatport" {
  account_id   = "beatport"
  display_name = "Beatport"
  description  = "Beatport ops service account"
}

resource "google_service_account" "deezer" {
  account_id   = "deezer"
  display_name = "Deezer"
  description  = "Deezer ops service account"
}

resource "google_service_account" "slack" {
  account_id   = "slackbot"
  display_name = "Slack bot"
  description  = "Slack bot service account"
}

resource "google_project_iam_binding" "logging" {
  for_each = {
    beatport = google_service_account.beatport.email,
    deezer   = google_service_account.deezer.email,
    slack    = google_service_account.slack.email,
  }

  project = var.project
  role    = "roles/logging.logWriter"
  members = [
    "serviceAccount:${each.value}"
  ]
}