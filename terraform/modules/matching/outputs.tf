output "topics" {
  value = [for _, topic in google_pubsub_topic.matching: topic.name]
}