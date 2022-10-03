resource "google_pubsub_topic" "topic" {
  name = var.name

  message_retention_duration = "86600s"
}

resource "google_pubsub_topic_iam_member" "publisher" {
  for_each = var.publishers

  topic  = google_pubsub_topic.topic.name
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:${each.value}"
}

resource "google_pubsub_topic_iam_member" "subscriber" {
  topic  = google_pubsub_topic.topic.name
  role   = "roles/pubsub.subscriber"
  member = "serviceAccount:${var.service_account}"
}