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

  min_instances = 1
  max_instances = 1
}
