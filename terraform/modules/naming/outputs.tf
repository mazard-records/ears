locals {
  project_id   = "mzr-${var.application}-${var.environment}"
  project_name = "${var.application}-${var.environment}"
}

locals {
  region_tokens    = split("-", var.region)
  region_primary   = substr(local.region_tokens[0], 0, 2)
  region_secondary = substr(substr(local.region_tokens[1], 0, -2), 0, 2)
  region_number    = substr(local.region_tokens[1], -1, 1)
}

locals {
  prefix = "mzr-${var.application}-${substr(var.environment, 0, 1)}"
  short_prefix = substr(var.environment, 0, 1)
  region = join("", [
    local.region_primary,
    local.region_secondary,
    local.region_number
  ])
  suffix = lower(terraform.workspace)
  region_suffix = join("-", [
    local.region,
    local.suffix
  ])
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

output "short_prefix" {
  value = local.short_prefix
}

output "region" {
  value = local.region
}

output "suffix" {
  value = local.suffix
}

output "region_suffix" {
  value = local.region_suffix
}

output "backend_service" {
  value = "${local.prefix}-cbs-%s-${local.region_suffix}"
}

output "signed_url_key" {
  value = "${local.prefix}-suk-%s-${local.region}-%s"
}

output "eventarc" {
  value = "${local.prefix}-eat-%s-${local.region_suffix}"
}

output "function" {
  value = "${local.prefix}-cfn-%s-${local.region_suffix}"
}

output "global_forwarding_rule" {
  value = "${local.prefix}-cfr-%s-${local.suffix}"
}

output "memorystore" {
  value = "${local.prefix}-msr-%s-${local.region_suffix}"
}

output "memorystore_default" {
  value = "${local.prefix}-msr-%s-${local.region}-default"
}

output "network_endpoint_group" {
  value = "${local.prefix}-neg-%s-${local.region_suffix}"
}

output "proxy" {
  value = "${local.prefix}-ctp-%s-${local.suffix}"
}

output "pubsub_topic" {
  value = "${local.prefix}-pst-%s-${local.region_suffix}"
}

output "run" {
  value = "${local.prefix}-run-%s-${local.region_suffix}"
}

output "secret" {
  value = "%s-${local.region_suffix}"
}

output "default_secret" {
  value = "%s-${local.region}-default"
}

output "sql_instance" {
  value = "${local.prefix}-sdi-%s-${local.region}-%s"
}

output "sql_database" {
  value = "${local.prefix}-sdb-%s-${local.region_suffix}"
}

output "compute_address" {
  value = "${local.prefix}-cad-%s-${local.suffix}"
}

output "compute_engine" {
  value = "${local.prefix}-cce-%s-${local.region_suffix}"
}

output "compute_instance" {
  value = "${local.prefix}-gci-%s-${local.region_suffix}"
}

output "compute_router" {
  value = "${local.prefix}-rte-%s-${local.region_suffix}"
}

output "compute_router_nat" {
  value = "${local.prefix}-nat-%s-${local.region_suffix}"
}

output "ssl" {
  value = "${local.prefix}-ssl-%s-${local.suffix}"
}

output "ssl_policy" {
  value = "${local.prefix}-spl-%s-${local.suffix}"
}

output "resource_storage_bucket" {
  value = "${local.prefix}-sbk-${local.region}-%s-%s"
}

output "storage_bucket" {
  value = "${local.prefix}-sbk-${local.region}-%s-${local.suffix}"
}

output "url_map" {
  value = "${local.prefix}-cum-%s-${local.suffix}"
}

output "vpc_address" {
  value = "${local.prefix}-cga-%s-${local.suffix}"
}

output "vpc_connector" {
  # NOTE: This resources name is limited to a 25 characters limit.
  #       To prevent from error we use short project prefix.
  value = "cac-%s-${local.region_suffix}"
}

output "vpc" {
  value = "${local.prefix}-vpc-%s-${local.suffix}"
}

output "workflow" {
  # NOTE: the only region workflows is available at the moment
  #       in Europe is west4.
  value = "${local.prefix}-wfw-%s-${local.region_suffix}"
}