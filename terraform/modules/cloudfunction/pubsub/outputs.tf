output "function" {
  value = google_cloudfunctions_function.target.name
}

output "topic" {
  value = google_pubsub_topic.topic.name
}