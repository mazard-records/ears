output "topics" {
  value = [for producer in var.producers: google_pubsub_topic.matching[producer].id]
}