output "topics" {
  value = [for topic in google_pubsub_topic.matching: topic.name]
}