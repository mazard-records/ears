module "naming" {
  source      = "../naming"
  application = var.application
  environment = var.environment
  region      = var.region
}