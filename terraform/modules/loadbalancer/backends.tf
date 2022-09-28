resource "google_compute_region_network_endpoint_group" "functions" {
  for_each = var.functions.targets

  name                  = format(module.naming.network_endpoint_group, "${each.key}")
  network_endpoint_type = "SERVERLESS"
  region                = module.naming.region

  cloud_function {
    function = each.value
  }
}

resource "google_compute_backend_service" "functions" {
  for_each = var.functions.targets

  name = format(module.naming.backend_service, each.key)

  backend {
    group = google_compute_region_network_endpoint_group.functions[each.key].self_link
  }
}
