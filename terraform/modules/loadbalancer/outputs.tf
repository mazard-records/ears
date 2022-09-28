output "IPv4" {
  value = google_compute_global_address.addresses["IPV4"].address
}

output "IPv6" {
  value = google_compute_global_address.addresses["IPV6"].address
}