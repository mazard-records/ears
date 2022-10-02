resource "google_pubsub_topic" "topic" {
  name = var.name

  message_retention_duration = "86600s"
}

resource "google_pubsub_topic_iam_member" "subscriber" {
  topic  = google_pubsub_topic.topic.name
  role   = "roles/pubsub.subscriber"
  member = "serviceAccount:${var.service_account}"
}