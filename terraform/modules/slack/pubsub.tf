resource "google_pubsub_topic_iam_member" "matching" {
  topic  = var.matching_topic
  role   = "roles/pubsub.subscriber"
  member = "serviceAccount:${google_service_account.slack.email}"
}