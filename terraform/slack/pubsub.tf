resource "google_pubsub_topic_iam_member" "matching" {
  for_each = toset(var.matching_topics)

  topic  = each.key
  role   = "roles/pubsub.subscriber"
  member = "serviceAccount:${google_service_account.slack.email}"
}