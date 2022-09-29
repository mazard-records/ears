resource "google_service_account" "matching" {
  for_each = toset(var.producers)

  account_id   = "matching-${each.key}"
  display_name = "${title(each.key)} matching"
  description  = "Matching compute for ${each.key} provider"
}

resource "google_project_iam_binding" "matching_log" {
  for_each = toset(var.producers)
  
  project = module.naming.project_id
  role    = "roles/logging.logWriter"
  members = [
    "serviceAccount:${google_service_account.matching[each.key].email}"
  ]
}