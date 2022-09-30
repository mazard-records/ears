resource "google_pubsub_topic" "beatport_matching" {
  name = format(module.naming.pubsub_topic, "beatport-matching")

  message_retention_duration = "86600s"
}