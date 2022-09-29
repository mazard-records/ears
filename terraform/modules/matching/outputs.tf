output "topics" {
  value = [for _, topic in google_pubsub_topic.matching: topic.name]
}

output "beatport_search_function" {
  value = google_cloudfunctions_function.beatport_search.name
}