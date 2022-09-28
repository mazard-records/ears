module "matching" {
  source = "../../modules/matching"

  environment = "development"
}

module "slack" {
  source      = "../../modules/slack"
  environment = "development"

  matching_topic = module.matching.topic
}

module "loadbalancer" {
  source = "../../modules/loadbalancer"

  environment = "development"
  functions   = {
    domains = [
      "dev.functions.mazard-records.fr"
    ]
    targets = {
      slack = module.slack.function
    }
  } 
}