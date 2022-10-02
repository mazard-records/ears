data "archive_file" "sources" {
  type        = "zip"
  source_dir  = "${path.module}/../../../../functions/${var.path}"
  output_path = "${path.module}/../../../../functions/${var.path}/build.zip"
}

resource "google_storage_bucket_object" "sources_archive" {
  name     = format("%s.zip", data.archive_file.sources.output_md5)
  bucket   = var.bucket
  source   = data.archive_file.sources.output_path
}

resource "google_cloudfunctions_function" "target" {
  name        = var.name
  description = var.description
  runtime     = "python39"

  environment_variables = var.envvars

  dynamic "secret_environment_variables" {
    for_each = var.secrets

    content {
      key     = each.key
      secret  = each.value
      version = "latest"
    }
  }

  available_memory_mb          = var.memory
  source_archive_bucket        = var.bucket
  source_archive_object        = google_storage_bucket_object.sources_archive.name
  entry_point                  = var.entrypoint
  service_account_email        = var.service_account
  trigger_http                 = null

  event_trigger {
    event_type = "providers/cloud.pubsub/eventTypes/topic.publish"
    resource   = google_pubsub_topic.topic.name  
  }

  max_instances = 1
}