module "slack_interactivity_webhook" {
  source = "../../cloudfunction/https"

  path   = "slack"
  bucket = google_storage_bucket.functions.name

  name            = "slack-interactivity-webhook"
  description     = "Slack webhook for receiving interactive user feedback"
  entrypoint      = "on_interactivity_webhook"
  ingress         = "ALLOW_ALL"
  service_account = google_service_account.slack.email
  all_users       = true

  secrets = {
    SLACK_SIGNING_KEY = google_secret_manager_secret.signing_secret.secret_id
    SLACK_WEBHOOK = google_secret_manager_secret.webhook.secret_id
  }

}

module "slack_command_webhook" {
  source = "../../cloudfunction/https"

  path   = "slack"
  bucket = google_storage_bucket.functions.name

  name            = "slack-command-webhook"
  description     = "Slack webhook for receiving user command"
  entrypoint      = "on_interactive_webhook"
  ingress         = "ALLOW_ALL"
  service_account = google_service_account.slack.email
  all_users       = true

  secrets = {
    SLACK_SIGNING_KEY = google_secret_manager_secret.signing_secret.secret_id
    SLACK_WEBHOOK = google_secret_manager_secret.webhook.secret_id
  }

}

module "deezer_update_playlist" {
  source = "../../cloudfunction/pubsub"

  path   = "deezer"
  bucket = google_storage_bucket.functions.name

  name            = "deezer-update-playlist"
  description     = "Update a target playlist on Deezer"
  entrypoint      = "on_update_playlist_event"
  service_account = google_service_account.beatport.email
  publishers      = [google_service_account.slack.service_account]

  envvars = {
    DEEEZER_WANTLIST = var.deezer_wantlist
  }

  secrets = {
    DEEZER_ACCESS_TOKEN = google_secret_manager_secret.deezer_access_token.secret_id
  }

}

module "beatport_update_playlist" {
  source = "../../cloudfunction/pubsub"

  path   = "beatport"
  bucket = google_storage_bucket.functions.name

  name            = "beatport-update-playlist"
  description     = "Update a target playlist on Beatport"
  entrypoint      = "on_update_playlist_event"
  service_account = google_service_account.beatport.email
  publishers      = [google_service_account.slack.service_account]

  envvars = {
    BEATPORT_WANTLIST = var.beatport_wantlist
  }

  secrets = {
    BEATPORT_USERNAME = google_secret_manager_secret.beatport_username.secret_id
    BEATPORT_PASSWORD = google_secret_manager_secret.beatport_password.secret_id
  }
}

module "beatport_search" {
  source = "../../cloudfunction/pubsub"

  path   = "beatport"
  bucket = google_storage_bucket.functions.name

  name            = "beatport-search-track"
  description     = "Search for a track using ears's protocol TrackSearchQuery input"
  entrypoint      = "on_search_event"
  service_account = google_service_account.beatport.email
}

module "slack_push_notification" {
  source = "../../cloudfunction/pubsub"

  path   = "slack"
  bucket = google_storage_bucket.functions.name

  name            = "slack-push-notification"
  description     = "Slack bot that produces interactive matching notification"
  entrypoint      = "on_push_notification_event"
  service_account = google_service_account.slack.email
  publishers      = [google_service_account.beatport.email]

  secrets = {
    SLACK_SIGNING_KEY = google_secret_manager_secret.signing_secret.secret_id
    SLACK_WEBHOOK = google_secret_manager_secret.webhook.secret_id
  }
}
