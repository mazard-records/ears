output "matching_notification_name" {
  value = google_cloudfunctions_function.slack_matching_notification.name
}

output "matching_notification_url" {
  value = google_cloudfunctions_function.slack_matching_notification.https_trigger_url
}

output "interactive_webhook_function" {
  value = google_cloudfunctions_function.slack_interactive_webhook.name
}