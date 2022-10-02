import json

from typing import Any

from ears.messaging import pydantic_model_from_event
from ears.models import TrackMatching
from ears.types import Event
from flask import Request, Response, jsonify
from pydantic import AnyHttpUrl, BaseSettings, Field
from slackette import (
    Actions,
    BlockInteraction,
    Blocks,
    Button,
    Divider,
    Image,
    Markdown,
    PlainText,
    Section,
    Style,
    SlackWebhook,
    verify_slack_signature,
)


class SlackSettings(BaseSettings):
    signing: str = Field(..., env="SLACK_SIGNING_KEY")
    version: str = Field("v0", env="SLACK_VERSION")
    webhook: AnyHttpUrl = Field(..., env="SLACK_WEBHOOK")

    @classmethod
    def signing_secret_provider(cls) -> str:
        return cls().signing
 

def TrackMatchingNotification(matching: TrackMatching) -> Blocks:
    """
    Build a rich interactive Slack notification using BlockKit
    to display the provided matched track entity.
    """
    return Blocks(blocks=[
        Divider(),
        Section(
            text=Markdown(
                text=(
                    f"{track.to_markdown_link()}\n"
                    f"*Release:*\n{matching.metadata.album}\n"
                    f"*Provider:*\n{matching.destination.provider}"
                )
            ),
            accessory=Image(image_url=matching.metadata.cover),
        ),
        Actions(
            elements=[
                Button(
                    style=Style.primary,
                    text=PlainText(text="Approve"),
                    value=matching.to_uri("validate")
                ),
                Button(
                    style=Style.danger,
                    text=PlainText(text="Deny"),
                    value=matching.to_uri("invalidate")
                ),
            ]
        )
    ])


@verify_slack_signature(signing_secret=SlackSettings.signing_secret_provider)
def on_command_webhook(request: Request) -> Response:
    """
    HTTP endpoint that provides command interactivity.
    """
    return jsonify(None)


@verify_slack_signature(signing_secret=SlackSettings.signing_secret_provider)
def on_interactive_webhook(request: Request) -> Response:
    """
    HTTP endpoint that acknowledge user feedback from Slack.
    """
    payload = request.form.get("payload", {})
    decoded = json.loads(payload)
    interaction = BlockInteraction(**decoded)
    # TODO: refactor this using protocol abstraction ?
    # router = InteractionRouter()
    # router.run(interaction)
    return jsonify(None)


def on_matching_event(event: Event, _: Any) -> None:
    settings = SlackSettings()
    matching = pydantic_model_from_event(TrackMatching, event)
    notification = TrackMatchingNotification(matching)
    webhook = SlackWebhook(settings.webhook)
    webhook(notification)
