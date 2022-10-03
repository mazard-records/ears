output "beatport_service_account" {
  value = google_service_account.beatport.email
}

output "deezer_service_account" {
  value = google_service_account.deezer.email
}