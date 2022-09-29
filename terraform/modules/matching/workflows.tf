locals {
  workflows = "${path.module}/../../../workflows"
  context   = {
    deezer = {
      access_token_secret = google_secret_manager_secret.deezer.name
    }
  }
}

resource "google_workflows_workflow" "matching" {
  for_each = toset(var.producers)

  description     = "Workflow that attempt to match tracks from Deezer to ${title(each.key)}"
  name            = format(module.naming.workflow, "${each.key}-matching")
  region          = module.naming.region
  service_account = google_service_account.matching[each.key].email
  source_contents = templatefile("${local.workflows}/matching-beatport.yaml", context)
}