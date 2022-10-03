from typing import Any, Callable, Dict, Type

from pydantic import BaseModel
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

from ears.messaging import pydantic_model_from_event
from ears.models import TrackMatching
from ears.types import Event, PydanticModel

ModelFactories = Dict[str, Type[BaseModel]]
BlockFactory = Callable[[BaseModel], Blocks]
BlocksFactories = Dict[str, BlockFactory]


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


_notification_factories = {
    TrackMatching: create_track_matching_notification,
}


class NotificationEvent(BaseModel):
    model: str
    data: Dict[str, Any]


def notification_from_event(event: Event) -> Blocks:
    notification = pydantic_model_from_event(NotificationEvent, event)
    for model, factory in _notification_factories.items():
        if model.__name__ == notification.model:
            return factory(model(**notification.data))
    raise ValueError(f"Unknown notification model {model.__name__}")
