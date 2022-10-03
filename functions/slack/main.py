from typing import Any

from commands import on_broadcast_command, on_buy_command
from flask import Request, Response, jsonify
from interactions import on_matching_feedback_request
from notifications import notification_from_event
from pydantic import AnyHttpUrl, BaseSettings, Field
from router import Router
from slackette import SlackWebhook, verify_slack_signature

from ears.types import Event


class SlackSettings(BaseSettings):
    signing: str = Field(..., env="SLACK_SIGNING_KEY")
    version: str = Field("v0", env="SLACK_VERSION")
    webhook: AnyHttpUrl = Field(..., env="SLACK_WEBHOOK")

    @classmethod
    def signing_secret_provider(cls) -> str:
        return cls().signing


@verify_slack_signature(
    signing_secret=SlackSettings.signing_secret_provider,
)
def on_command_webhook(request: Request) -> Response:
    """
    HTTP endpoint that provides command interactivity.
    """
    router = Router()
    router.register_command("broadcast", on_broadcast_command)
    router.register_command("buy", on_buy_command)
    response = router.serve_command_request(request)
    if isinstance(response, Response):
        return response
    return jsonify(response)


@verify_slack_signature(
    signing_secret=SlackSettings.signing_secret_provider,
)
def on_interactivity_webhook(request: Request) -> Response:
    """
    HTTP webhook for Slack interactivity callback. Evaluate actions
    payload as internal protocol to trigger associated handlers.
    """
    router = Router()
    router.register_interaction("matching", on_matching_feedback_request)
    router.serve_interaction_request(request)
    return jsonify(None)


def on_push_notification_event(event: Event, _: Any) -> None:
    """
    PubSub entrypoint for pushing notification from registered
    Blocks factory.
    """
    notification = notification_from_event(event)
    settings = SlackSettings()
    webhook = SlackWebhook(settings.webhook)
    webhook(notification)
