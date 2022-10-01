resource "google_pubsub_topic" "matching" {
  name = "beatport-matching"

  message_retention_duration = "86600s"
}

resource "google_pubsub_topic_iam_member" "matching" {
  for_each = toset(var.publishers)

  topic  = google_pubsub_topic.matching
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:${google_service_account.slack.email}"
}