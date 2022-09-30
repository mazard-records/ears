import json
import logging

from functools import lru_cache
from typing import Callable
from urllib.parse import urlparse

from flask import Request, Response, jsonify
from google.cloud.logging import Client as LoggingClient
from httpx import post
from pydantic import AnyHttpUrl, BaseSettings, Field
from slackette import (
    BlockInteraction,
    InteractionResponse,
    SlackWebhook,
    verify_slack_signature
)

from matching import (
    MatchingTrack,
    MatchingTrackNotification,
    on_matching_action,
)

client = LoggingClient()
client.setup_logging(log_level=logging.DEBUG)


class _Settings(BaseSettings):
    signing: str = Field(..., env="SLACK_SIGNING_KEY")
    version: str = Field("v0", env="SLACK_VERSION")
    webhook: AnyHttpUrl = Field(..., env="SLACK_WEBHOOK")


class _InteractionRouter(object):
    """ Router for interactive callback. """

    def __init__(self) -> None:
        self._domain_handlers = {}

    def add_domain_handler(
        self,
        domain: str,
        handler: Callable[[str], str],
    ) -> None:
        self._domain_handlers[domain] = handler

    def run(self, interaction: BlockInteraction) -> None:
        for action in interaction.actions:
            url = urlparse(action.value)
            if url.scheme != "ears":
                raise ValueError(f"Invalid url scheme {url.scheme}")
            if url.netloc not in self._domain_handlers:
                raise ValueError(f"Invalid domain {url.scheme}")
            _ = self._domain_handlers[url.netloc](url.path)
            response = post(
                interaction.response_url,
                json={"delete_original": True},
            )
            response.raise_for_status()


@lru_cache(maxsize=1)
def Settings() -> _Settings:
    return _Settings()


@lru_cache(maxsize=1)
def InteractionRouter() -> None:
    router = _InteractionRouter()
    router.add_domain_handler("matching", on_matching_action)
    return router


def signing_secret_provider() -> str:
    return Settings().signing


def on_matching_event(request: Request) -> Response:
    """
    HTTP endpoint that publishes a Slack interactive
    notification when a track matching is received.
    """
    track = MatchingTrack(**request.get_json())
    notification = MatchingTrackNotification(track)
    webhook = SlackWebhook(Settings().webhook)
    webhook(notification)
    return jsonify(None)


@verify_slack_signature(signing_secret=signing_secret_provider)
def on_interactive_webhook(request: Request) -> Response:
    """
    HTTP endpoint that acknowledge user feedback from Slack.
    """
    payload = request.form.get("payload", {})
    decoded = json.loads(payload)
    interaction = BlockInteraction(**decoded)
    router = InteractionRouter()
    router.run(interaction)
    return jsonify(None)
