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
  ingress_settings             = var.ingress
  service_account_email        = var.service_account
  trigger_http                 = true
  https_trigger_security_level = "SECURE_ALWAYS"

  max_instances = 1
}

resource "google_cloudfunctions_function_iam_member" "invokers" {
  for_each = toset(var.invokers)

  cloud_function = google_cloudfunctions_function.target.name
  role           = "roles/cloudfunctions.invoker"
  member         = "serviceAccount:${each.key}"
}

resource "google_cloudfunctions_function_iam_member" "allUsers" {
  count = var.all_users ? 1 : 0

  cloud_function = google_cloudfunctions_function.target.name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers"
}
