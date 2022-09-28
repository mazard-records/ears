locals {
  domains = concat(
    var.functions.domains,
  )
}

resource "google_compute_global_address" "addresses" {
  for_each   = toset(["IPV4", "IPV6"])

  name       = format(module.naming.vpc_address,  "lb${lower(each.key)}")
  ip_version = "IPV4"
}

resource "google_compute_managed_ssl_certificate" "certificates" {
  name = format(module.naming.ssl, "certificates")

  managed {
    domains = toset(local.domains)
  }
}

resource "google_compute_ssl_policy" "modern" {
  name            = format(module.naming.ssl_policy, "modern")
  profile         = "MODERN"
  min_tls_version = "TLS_1_2"
}

resource "google_compute_target_https_proxy" "https" {
  name    = format(module.naming.proxy, "https")

  url_map          = google_compute_url_map.primary.id
  ssl_certificates = [google_compute_managed_ssl_certificate.certificates.id]
  ssl_policy       = google_compute_ssl_policy.modern.id
}

resource "google_compute_target_http_proxy" "http_proxy" {
  name    = format(module.naming.proxy, "http")

  url_map = google_compute_url_map.http_redirect.id
}

resource "google_compute_global_forwarding_rule" "https_forwarding_rule" {
  for_each = google_compute_global_address.addresses

  name       = format(module.naming.global_forwarding_rule, "https${each.key}")
  target     = google_compute_target_https_proxy.https.id
  ip_address = each.value.address
  port_range = "443"
}

resource "google_compute_global_forwarding_rule" "http_forwarding_rule" {
  for_each = google_compute_global_address.addresses

  name       = format(module.naming.global_forwarding_rule, "http${each.key}")
  target     = google_compute_target_http_proxy.http_proxy.id
  ip_address = each.value.address
  port_range = "80"
}