locals {
  project_id   = "mzr-${var.application}-${var.environment}"
  project_name = "${var.application}-${var.environment}"
  prefix       = "mzr-${var.application}-${substr(var.environment, 0, 1)}"
}

output "project_id" {
  value = local.project_id
}

output "project_name" {
  value = local.project_name
}

output "prefix" {
  value = local.prefix
}

output "region" {
  value = var.region
}

output "backend_service" {
  value = "${local.prefix}-cbs-%s"
}

output "eventarc" {
  value = "${local.prefix}-eat-%s"
}

output "function" {
  value = "${local.prefix}-cfn-%s"
}

output "global_forwarding_rule" {
  value = "${local.prefix}-cfr-%s"
}

output "memorystore" {
  value = "${local.prefix}-msr-%s"
}

output "memorystore_default" {
  value = "${local.prefix}-msr-%s"
}

output "network_endpoint_group" {
  value = "${local.prefix}-neg-%s"
}

output "proxy" {
  value = "${local.prefix}-ctp-%s"
}

output "pubsub_topic" {
  value = "${local.prefix}-pst-%s"
}

output "run" {
  value = "${local.prefix}-run-%s"
}

output "secret" {
  value = "%s"
}

output "default_secret" {
  value = "%s-${local.region}"
}

output "sql_instance" {
  value = "${local.prefix}-sdi-%s"
}

output "sql_database" {
  value = "${local.prefix}-sdb-%s"
}

output "compute_address" {
  value = "${local.prefix}-cad-%s"
}

output "compute_engine" {
  value = "${local.prefix}-cce-%s"
}

output "compute_instance" {
  value = "${local.prefix}-gci-%s"
}

output "compute_router" {
  value = "${local.prefix}-rte-%s"
}

output "compute_router_nat" {
  value = "${local.prefix}-nat-%s"
}

output "ssl" {
  value = "${local.prefix}-ssl-%s"
}

output "ssl_policy" {
  value = "${local.prefix}-spl-%s"
}

output "resource_storage_bucket" {
  value = "${local.prefix}-sbk-%s"
}

output "storage_bucket" {
  value = "${local.prefix}-sbk-%s"
}

output "url_map" {
  value = "${local.prefix}-cum-%s"
}

output "vpc_address" {
  value = "${local.prefix}-cga-%s"
}

output "vpc_connector" {
  # NOTE: This resources name is limited to a 25 characters limit.
  #       To prevent from error we use short project prefix.
  value = "cac-%s"
}

output "vpc" {
  value = "${local.prefix}-vpc-%s"
}

output "workflow" {
  # NOTE: the only region workflows is available at the moment
  #       in Europe is west4.
  value = "${local.prefix}-wfw-%s"
}