resource "google_pubsub_topic" "beatport" {
  name = "mzr-ears-p-pst-beatport"
}

resource "google_pubsub_topic_iam_member" "publisher" {
  topic  = google_pubsub_topic.beatport.name
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:${google_service_account.publisher.email}"
}