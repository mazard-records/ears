locals {
  workflows = "${path.module}/../../workflows"
}

resource "google_workflows_workflow" "matching" {
  for_each = var.providers

  description     = "Workflow that attempt to match tracks from Deezer to ${title(each.key)}"
  name            = format(module.naming.workflow, "${each.key}-matching")
  region          = var.region
  service_account = google_service_account.matching[each.key].email
  source_contents = file("${workflows}/matching-beatport.yaml")
}