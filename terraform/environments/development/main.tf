module "ears" {
  source      = "../../modules/project"

  application           = "ears"
  environment           = var.environment
  cloudstorage_location = var.cloudstorage_location
  domain                = var.domain
  redirect_url          = var.redirect_url
  region                = var.region

  beatport_wantlist = var.beatport_wantlist
}