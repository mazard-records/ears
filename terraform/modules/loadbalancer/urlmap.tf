resource "google_compute_url_map" "primary" {
  name        = format(module.naming.url_map, "primary")
  description = "Global URL map for service routing"

  default_url_redirect {
    host_redirect          = var.redirect_url
    redirect_response_code = "PERMANENT_REDIRECT"
    strip_query            = false
  }

  host_rule {
    hosts        = var.functions.domains
    path_matcher = "functions"
  }

  path_matcher {
    name = "functions"

    dynamic "path_rule" {
      for_each = var.functions.targets
      
      content {
        paths   = path_rule.key
        service = google_compute_backend_service.functions[path_rule.key]
      }
    }
  }

}

resource "google_compute_url_map" "http_redirect" {
  name    = format(module.naming.url_map, "http")

  default_url_redirect {
    https_redirect         = true
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT"
    strip_query            = false
  }
}