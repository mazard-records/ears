from typing import Any, Dict, cast

from pydantic import BaseSettings, Field
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

from ears.events import PlaylistAction, PlaylistEvent
from ears.messaging import publish
from ears.models import Resource, ResourceType, TrackMatching


def _create_matching_url(matching: TrackMatching, action: str) -> str:
    return (
        f"ears://matching/{action}"
        f"/{matching.origin.to_urn()}"
        f"/{matching.destination.to_urn()}"
    )


def create_track_matching_notification(matching: TrackMatching) -> Blocks:
    """
    Build a rich interactive Slack notification using BlockKit
    to display the provided matched track entity.
    """
    if matching.metadata is None:
        raise ValueError("Cannot notify empty metadata")
    return Blocks(
        blocks=[
            Divider(),
            Section(
                text=Markdown(
                    text=(
                        f"*<{matching.destination.url}"
                        f"|{matching.metadata.title} - {matching.metadata.artist}>*\n"
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
                        value=_create_matching_url(matching, "validate"),
                    ),
                    Button(
                        style=Style.danger,
                        text=PlainText(text="Deny"),
                        value=_create_matching_url(matching, "invalidate"),
                    ),
                ]
            ),
        ]
    )


class MatchingPlaylists(BaseSettings):
    beatport: int = Field(..., env="WANTLIST_BEATPORT")
    deezer: int = Field(..., env="WANTLIST_DEEZER")

    def by_provider(self, name: str) -> Any:
        schema = self.__class__.schema()
        properties = cast(Dict[str, Any], schema.get("properties"))
        if name not in properties:
            raise ValueError(f"Unknown provider wantlist {name}")
        return getattr(self, name)


def on_matching_feedback_request(path: str) -> None:
    """
    Domain handler for InteractionRouter which acknowledge matching
    action and publish a message into a Pub/Sub topic accordingly.
    """
    tokens = path.split("/")
    # NOTE: url start with / so we have an empty token.
    if len(tokens) != 4:
        raise ValueError("Invalid matching URL")
    action = tokens[1]
    matching = TrackMatching(
        origin=Resource.from_urn(tokens[2]),
        destination=Resource.from_urn(tokens[3]),
    )
    playlists = MatchingPlaylists()
    if action == "validate":
        publish(
            f"{matching.destination.provider}-update-playlist",
            PlaylistEvent(
                action=PlaylistAction.add,
                playlist_urn=Resource(
                    id=playlists.by_provider(matching.destination.provider),
                    provider=matching.destination.provider,
                    type=ResourceType.playlist,
                ).to_urn(),
                track_urn=matching.destination.to_urn(),
            ),
        )
        publish(
            f"{matching.origin.provider}-update-playlist",
            PlaylistEvent(
                action=PlaylistAction.remove,
                playlist_urn=Resource(
                    id=playlists.by_provider(matching.origin.provider),
                    provider=matching.origin.provider,
                    type=ResourceType.playlist,
                ).to_urn(),
                track_urn=matching.origin.to_urn(),
            ),
        )
    elif action == "invalidate":
        # TODO: publish to alternative topic
        pass
    else:
        raise ValueError("Invalid matching action")
