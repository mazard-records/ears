import json
import logging

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import AnyHttpUrl, BaseModel
from slackette import (
    Actions,
    Blocks,
    Button,
    Divider,
    Image,
    Markdown,
    PlainText,
    Section,
    Style,
)

class Provider(str, Enum):
    beatport = "beatport"


class MatchingSource(BaseModel):
    identifier: Any
    provider: str
    url: Optional[AnyHttpUrl] = None

    @classmethod
    def from_urn(cls, urn: str) -> "MatchingSource":
        tokens = urn.split(":")
        if len(tokens) != 3 or tokens[0] != "urn":
            raise ValueError(f"Invalid urn {urn}")
        return cls(identifier=tokens[2], provider=tokens[1])

    def to_urn(self) -> str:
        return f"urn:{self.provider}:{self.identifier}"


class MatchingTrack(BaseModel):
    origin: MatchingSource
    destination: MatchingSource
    album: str
    artist: str
    title: str
    cover: AnyHttpUrl
    preview: Optional[AnyHttpUrl]

    def to_markdown_link(self) -> str:
        return f"*<{self.destination.url}|{self.title} - {self.artist}>*"

    def to_uri(self, action: str) -> str:
        return (
            f"ears://matching/{action}"
            f"/{self.origin.to_urn()}"
            f"/{self.destination.to_urn()}"
        )


def MatchingTrackNotification(track: MatchingTrack) -> Blocks:
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
                    f"*Release:*\n{track.album}\n"
                    f"*Provider:*\n{track.destination.provider}"
                )
            ),
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


def on_matching_action(url: str) -> Optional[str]:
    """
    Domain handler for InteractionRouter which acknowledge matching
    action and publish a message into a Pub/Sub topic accordingly.
    """
    tokens = url.split("/")
    # NOTE: url start with / so we have an empty token.
    if len(tokens) != 4:
        raise ValueError("Invalid matching URL")
    action = tokens[1]
    origin = MatchingSource.from_urn(tokens[2])
    destination = MatchingSource.from_urn(tokens[3])
    producer = MessageProducer(destination.provider)
    if action == "validate":
        producer({"id": destination.identifier})
    elif action == "invalidate":
        logging.debug(
            f"Deny matching {origin.provider}#{origin.identifier}"
            f" -> {destination.provider}#{destination.identifier}"
        )
    else:
        raise ValueError("Invalid action")



publisher = PublisherClient()
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    topic='MY_TOPIC_NAME',  # Set this to something appropriate.
)
future = publisher.publish(topic_name, b'My first message!', spam='eggs')
future.result()