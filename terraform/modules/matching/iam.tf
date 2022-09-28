resource "google_service_account" "matching" {
  for_each = var.producers

  account_id   = "matching-${each.key}"
  display_name = "${title(each.key)} matching"
  description  = "Matching compute for ${each.key} provider"
}