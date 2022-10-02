from ears.messaging import EventPublisher
from ears.models import Resource, TrackMatching
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


def _create_matching_url(matching: TrackMatching, action: str) -> str:
    return (
        f"ears://matching/{action}"
        f"/{matching.origin.to_urn()}"
        f"/{matching.destination.to_urn()}"
    )


def _create_matching_markdown_link(matching: TrackMatching) -> str:
    return f"*<{matching.destination.url}|{matching.title} - {matching.artist}>*"


def create_track_matching_notification(matching: TrackMatching) -> Blocks:
    """
    Build a rich interactive Slack notification using BlockKit
    to display the provided matched track entity.
    """
    return Blocks(blocks=[
        Divider(),
        Section(
            text=Markdown(
                text=(
                    f"{_create_matching_markdown_link(matching)}\n"
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
                    value=_create_matching_url(matching, "validate")
                ),
                Button(
                    style=Style.danger,
                    text=PlainText(text="Deny"),
                    value=_create_matching_url(matching, "invalidate")
                ),
            ]
        )
    ])


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
    publisher = EventPublisher(
        f"{matching.destination.provider}-update-playlist"
    )
    if action == "validate":
        publisher(matching)
    elif action == "invalidate":
        # TODO: publish to alternative topic
        pass
    else:
        raise ValueError("Invalid matching action")
