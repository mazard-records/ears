# EARS: Easy Acquisition of Recommanded Sounds

[![Main](https://github.com/mazard-records/ears/actions/workflows/main.yaml/badge.svg)](https://github.com/mazard-records/ears/actions/workflows/main.yaml)
[![PyPI version](https://badge.fury.io/py/ears.svg)](https://badge.fury.io/py/ears)

EARS is an event driven system for managing music acquisition on multiple
platforms. It uses streaming playlist as data source and trigger various
track matching with user interaction made through Slack ops.

> :warning: documentation is not available yet.

## Providers

The following table list supported music providers:

| Type        | Provider |
| ----------- | -------- |
| Datasource  | Deezer   |
| Acquisition | Beatport |

## Deploy your custom instance with Terraform

My personal instance is deployed using Terraform Cloud, but you can deploy
your own by running Terraform locally:

```bash
$ git clone https://github.com/mazard-records/ears
$ cd ears/terraform
$ terraform init
$ terraform apply -auto-approve
```

> :warning: First deployment will fail as created secrets would not be filled.
> You will need to fill secrets and then rerun deployment process.

You will need to set following variables to make it work:

| Name | Description |
| ---- | ----------- |
| `project`           | Target GCP project id |
| `region`            | Target region for resources (default to `europe-west1`) |
| `beatport_wantlist` | Identifier of the Beatport playlist that will receive matching |
| `deezer_wantlist`   | Identifier of the Deezer playlist that acts as source |

The terraform configuration will output various URL that you will need to use
in order to configure your dedicated Slack application to work.