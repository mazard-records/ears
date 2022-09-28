locals {
  workflows = "${path.module}/../../workflows"
}

resource "google_workflows_workflow" "matching" {
  for_each = toset(var.producers)

  description     = "Workflow that attempt to match tracks from Deezer to ${title(each.key)}"
  name            = format(module.naming.workflow, "${each.key}-matching")
  region          = module.naming.region
  service_account = google_service_account.matching[each.key].email
  source_contents = file("${local.workflows}/matching-beatport.yaml")
}