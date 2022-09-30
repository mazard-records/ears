output "beatport_search_function" {
  value = google_cloudfunctions_function.beatport_search.name
}

output "matching_topics" {
  value = [
    google_pubsub_topic.beatport_matching.name,
  ]
}