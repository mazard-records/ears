module "matching" {
  source = "../../modules/matching"

  environment = "production"
}

module "slack" {
  source      = "../../modules/slack"
  environment = "production"

  matching_topic = module.matching.topic
}

module "loadbalancer" {
  source = "../../modules/loadbalancer"

  environment = "production"
  functions   = {
    domains = [
      "functions.mazard-records.fr"
    ]
    targets = {
      slack = module.slack.function
    }
  } 
}