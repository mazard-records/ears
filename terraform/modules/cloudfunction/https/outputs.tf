output "function" {
  value = google_cloudfunctions_function.target.name
}

output "url" {
  value = google_cloudfunctions_function.target.https_trigger_url
}