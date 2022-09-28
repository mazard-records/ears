from typing import Any, Dict

from flask import Request, Response, jsonify
from httpx import post
from pydantic import AnyHttpUrl, BaseSettings

from .blocks import *
from .providers import MatchingTrack


class SlackSettings(BaseSettings):
    SLACK_MATCHING_WEBHOOK: AnyHttpUrl


def MatchingTrackNotification(track: MatchingTrack) -> Blocks:
    """
    Build a rich interactive Slack notification using BlockKit
    to display the provided matched track entity.
    """
    return Blocks(blocks=[
        Section(
            text=Markdown(text=track.to_markdown_link()),
            accessory=Image(image_url=track.cover),
        ),
        Actions(
            elements=[
                Button(
                    style=Style.primary,
                    text=PlainText(text="Approve"),
                    value=track.to_uri("validate")
                ),
                Button(
                    style=Style.danger,
                    text=PlainText(text="Deny"),
                    value=track.to_uri("invalidate")
                ),
            ]
        )
    ])


def on_matching_event(event: Dict[str, Any], _: Any) -> None:
    """
    PubSub entrypoint that publishes a Slack interactive
    notification when a track matching is received.
    """
    settings = SlackSettings()
    track = MatchingTrack.from_event(event)
    notification = MatchingTrackNotification(track)
    response = post(settings.SLACK_MATCHING_WEBHOOK, json=notification.dict())
    # TODO: error handling with CloudLogging.
    response.raise_for_status()


def on_interactive_webhook(request: Request) -> Response:
    """
    HTTP endpoint that acknowledge user feedback from Slack.
    """
    # TODO: prevent from unallowed access;
    # TODO: create payload model and evaluate result.
    print(request.get_json())
    return jsonify(None)
