data "archive_file" "slack" {
  type        = "zip"
  source_dir  = "${path.module}/../../../functions/slack"
  output_path = "${path.module}/../../../functions/slack/build.zip"
}

data "google_storage_bucket" "functions" {
  name = format(module.naming.storage_bucket, "functions")
}

resource "google_storage_bucket_object" "slack" {
  name     = format("%s.zip", data.archive_file.slack.output_md5)
  bucket   = data.google_storage_bucket.functions.name
  source   = data.archive_file.slack.output_path
}

resource "google_cloudfunctions_function" "slack_matching_notification" {
  name        = format(module.naming.function, "slack-matching-notification")
  description = "Slack bot for interactive matching notification"
  runtime     = "python39"

  secret_environment_variables {
    key     = "SLACK_MATCHING_WEBHOOK"
    secret  = google_secret_manager_secret.slack_webhook.secret_id
    version = "latest"
  }

  available_memory_mb   = 64
  source_archive_bucket = data.google_storage_bucket.functions.name
  source_archive_object = google_storage_bucket_object.slack.name
  entry_point           = "on_matching_event"
  ingress_settings      = "ALLOW_INTERNAL_ONLY"
  service_account_email = google_service_account.slack.email
  trigger_http          = null
 
  event_trigger {
    event_type = "providers/cloud.pubsub/eventTypes/topic.publish"
    resource   = var.matching_topic
  }
}

resource "google_cloudfunctions_function" "slack_interactive_webhook" {
  name        = format(module.naming.function, "slack-interactive-webhook")
  description = "Slack webhook for receiving interactive user feedback"
  runtime     = "python39"

  secret_environment_variables {
    key     = "SLACK_MATCHING_WEBHOOK"
    secret  = google_secret_manager_secret.slack_webhook.secret_id
    version = "latest"
  }

  available_memory_mb   = 128
  source_archive_bucket = data.google_storage_bucket.functions.name
  source_archive_object = google_storage_bucket_object.slack.name
  entry_point           = "on_interactive_webhook"
  ingress_settings      = "ALLOW_INTERNAL_ONLY"
  service_account_email = google_service_account.slack.email
  trigger_http          = true
}