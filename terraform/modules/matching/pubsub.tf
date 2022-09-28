resource "google_pubsub_topic" "matching" {
  for_each = var.providers

  name = format(module.naming.pubsub_topic, "matching-${each.key}")
}

resource "google_pubsub_topic_iam_member" "producers" {
  for_each = var.providers

  topic  = google_pubsub_topic.matching[each.key].name
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:${google_service_account.matching[each.key].email}"
}
