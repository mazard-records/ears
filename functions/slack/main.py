import json
from functools import lru_cache
from typing import Any

from domains.matching import (
    create_track_matching_notification,
    on_matching_feedback_request,
)
from flask import Request, Response, jsonify
from httpx import post
from notifications import NotificationFactory
from pydantic import AnyHttpUrl, BaseSettings, Field
from router import Router
from slackette import (
    BlockInteraction,
    InteractionDeleteResponse,
    SlackWebhook,
    verify_slack_signature,
)

from ears.models import TrackMatching
from ears.types import Event


class SlackSettings(BaseSettings):
    signing: str = Field(..., env="SLACK_SIGNING_KEY")
    version: str = Field("v0", env="SLACK_VERSION")
    webhook: AnyHttpUrl = Field(..., env="SLACK_WEBHOOK")

    @classmethod
    def signing_secret_provider(cls) -> str:
        return cls().signing


@lru_cache(maxsize=1)
def get_interactivity_router() -> Router:
    router = Router()
    router.register("matching", on_matching_feedback_request)
    # NOTE: add additional interactivity handler here.
    return router


@lru_cache(maxsize=1)
def get_notification_factory() -> NotificationFactory:
    factory = NotificationFactory()
    factory.register(TrackMatching, create_track_matching_notification)  # type: ignore
    # NOTE: add additional notification factory here.
    return factory


@verify_slack_signature(signing_secret=SlackSettings.signing_secret_provider)
def on_command_webhook(request: Request) -> Response:
    """
    HTTP endpoint that provides command interactivity.
    """
    return jsonify(None)


@verify_slack_signature(signing_secret=SlackSettings.signing_secret_provider)
def on_interactivity_webhook(request: Request) -> Response:
    """
    HTTP webhook for Slack interactivity callback. Evaluate actions
    payload as internal protocol to trigger associated handlers.
    """
    payload = request.form.get("payload", {})
    decoded = json.loads(payload)
    interaction = BlockInteraction(**decoded)
    router = get_interactivity_router()
    try:
        for action in interaction.actions:
            router.serve(action.value)
        response = post(
            interaction.response_url,
            json=InteractionDeleteResponse().dict(),
        )
        response.raise_for_status()
    except Exception as e:
        # TODO: process with feedback / log.
        # TODO: return error response.
        pass
    return jsonify(None)


def on_push_notification_event(event: Event, _: Any) -> None:
    """
    PubSub entrypoint for pushing notification from registered
    Blocks factory.
    """
    factory = get_notification_factory()
    notification = factory.create(event)
    settings = SlackSettings()
    webhook = SlackWebhook(settings.webhook)
    webhook(notification)
