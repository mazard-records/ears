data "archive_file" "beatport" {
  type        = "zip"
  source_dir  = "${path.module}/../../../functions/beatport"
  output_path = "${path.module}/../../../functions/beatport/build.zip"
}

resource "google_storage_bucket_object" "beatport" {
  name     = format("%s.zip", data.archive_file.beatport.output_md5)
  bucket   = var.function_bucket_name
  source   = data.archive_file.beatport.output_path
}

resource "google_cloudfunctions_function" "beatport_search" {
  name        = format(module.naming.function, "beatport-search")
  description = "Search track on Beatport"
  runtime     = "python39"

  dynamic "secret_environment_variables" {
    for_each = google_secret_manager_secret.beatport

    content {
      key     = "BEATPORT_${upper(secret_environment_variables.key)}"
      secret  = secret_environment_variables.value.secret_id
      version = "latest"
    }
  }

  available_memory_mb          = 128
  source_archive_bucket        = var.function_bucket_name
  source_archive_object        = google_storage_bucket_object.beatport.name
  entry_point                  = "on_search_request"
  ingress_settings             = "ALLOW_INTERNAL_ONLY"
  service_account_email        = google_service_account.matching["beatport"].email
  trigger_http                 = true
  https_trigger_security_level = "SECURE_ALWAYS"

  max_instances = 1
}

resource "google_cloudfunctions_function_iam_member" "beatport_search" {
  cloud_function = google_cloudfunctions_function.beatport_search.name
  role           = "roles/cloudfunctions.invoker"
  member         = "serviceAccount:${google_service_account.matching["beatport"].email}"
}

resource "google_cloudfunctions_function_iam_member" "slack" {
  cloud_function = var.slack_matching_notification_name
  role           = "roles/cloudfunctions.invoker"
  member         = "serviceAccount:${google_service_account.matching["beatport"].email}"
}

resource "google_cloudfunctions_function" "beatport_matching" {
  name        = format(module.naming.function, "beatport-matching")
  description = "Add matched track on Beatport"
  runtime     = "python39"

  environment_variables = {
    BEATPORT_WANTLIST = var.beatport_wantlist
  }

  dynamic "secret_environment_variables" {
    for_each = google_secret_manager_secret.beatport

    content {
      key     = "BEATPORT_${upper(secret_environment_variables.key)}"
      secret  = secret_environment_variables.value.secret_id
      version = "latest"
    }
  }

  available_memory_mb          = 128
  source_archive_bucket        = var.function_bucket_name
  source_archive_object        = google_storage_bucket_object.beatport.name
  entry_point                  = "on_wantlist_event"
  ingress_settings             = "ALLOW_INTERNAL_ONLY"
  service_account_email        = google_service_account.matching["beatport"].email
  trigger_http                 = null

  event_trigger {
    event_type = "providers/cloud.pubsub/eventTypes/topic.publish"
    resource   = google_pubsub_topic.beatport_matching.name
  }

  max_instances = 1
}