output "topics" {
  value = [for index, topic in google_pubsub_topic.matching: topic.name]
}