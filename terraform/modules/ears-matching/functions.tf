module "deezer_update_playlist" {
  source = "../../cloudfunction/pubsub"

  path   = "deezer"
  bucket = var.function_bucket

  name            = "deezer-update-playlist"
  description     = "Update a target playlist on Deezer"
  entrypoint      = "on_update_playlist_event"
  service_account = google_service_account.beatport.email
  publishers      = var.publishers

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
  bucket = var.function_bucket

  name            = "beatport-update-playlist"
  description     = "Update a target playlist on Beatport"
  entrypoint      = "on_update_playlist_event"
  service_account = google_service_account.beatport.email
  publishers      = var.publishers

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
  bucket = var.function_bucket

  name            = "beatport-search-track"
  description     = "Search for a track using ears's protocol TrackSearchQuery input"
  entrypoint      = "on_search_event"
  service_account = google_service_account.beatport.email
}
