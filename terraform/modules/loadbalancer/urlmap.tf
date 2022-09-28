resource "google_compute_url_map" "primary" {
  name        = format(module.naming.url_map, "primary")
  description = "Global URL map for service routing"
  default_service = google_compute_backend_service.home.id

  host_rule {
    hosts        = var.functions.domains
    path_matcher = "functions"
  }

  path_matcher {
    name = "functions"
    default_service = google_compute_backend_service.home.id

    dynamic "path_rule" {
      for_each = var.functions.targets
      
      content {
        paths   = path_rule.key
        service = google_compute_backend_service.functions[path_rule.key]
      }
    }
  }

}