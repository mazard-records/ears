output "service_account" {
  value = google_service_account.slack.email
}

output "command_webhook_url" {
  value = module.command_webhook.url
}

output "interactivity_wehbook_url" {
  value = module.interactivity_webhook.url
}

output "push_notification_topic" {
  value = module.push_notification.topic
}