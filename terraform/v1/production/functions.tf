data "archive_file" "functions" {
  for_each    = toset(["beatport"])
  type        = "zip"
  source_dir  = "${path.module}/../functions/${each.key}"
  output_path = "${path.module}/../functions/${each.key}/build.zip"
}

resource "google_storage_bucket_object" "functions" {
  for_each = toset(["beatport"])
  name     = format("%s.zip", data.archive_file.functions[each.key].output_md5)
  bucket   = google_storage_bucket.functions.name
  source   = data.archive_file.functions[each.key].output_path
}

resource "google_cloudfunctions_function" "beatport" {
  name        = "mzr-ears-p-cfn-beatport"
  description = "Beatport remote control function"
  runtime     = "python39"

  environment_variables = {
    WANTLIST = var.beatport_wantlist
  }

  dynamic "secret_environment_variables" {
    for_each = toset(["username", "password"])

    content {
      key        = secret_environment_variables.key
      secret     = google_secret_manager_secret.beatport[secret_environment_variables.key].secret_id
      version    = "latest"
    }
  }

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.functions.name
  source_archive_object = google_storage_bucket_object.functions["beatport"].name
  entry_point           = "entrypoint"
  ingress_settings      = "ALLOW_INTERNAL_ONLY"
  service_account_email = google_service_account.beatport.email

  event_trigger {
    event_type = "providers/cloud.pubsub/eventTypes/topic.publish"
    resource   = "${google_pubsub_topic.beatport.name}"
  }
}