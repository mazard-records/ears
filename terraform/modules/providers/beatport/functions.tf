module "search" {
  source = "../../cloudfunction/https"

  path   = "beatport"
  bucket = var.function_bucket

  name            = "beatport-search"
  description     = "Search for a track using ears's protocol TrackSearchQuery input"
  entrypoint      = "on_search_request"
  service_account = google_service_account.beatport.email
  invokers        = [google_service_account.beatport.email]
}

module "wantlist" {
  source = "../../cloudfunction/pubsub"

  path   = "beatport"
  bucket = var.function_bucket

  name            = "beatport-playlist"
  description     = "Add a given track to a target playlist"
  entrypoint      = "on_wantlist_event"
  service_account = google_service_account.beatport.email
  topics          = [google_pubsub_topic.beatport_matching.name]

  envvars = {
    BEATPORT_WANTLIST = var.beatport_wantlist
  }

  secrets = {
    BEATPORT_USERNAME = google_secret_manager_secret.beatport["username"].secret_id
    BEATPORT_PASSWORD = google_secret_manager_secret.beatport["password"].secret_id
  }
}