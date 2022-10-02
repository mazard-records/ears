from typing import Any

from pydantic import BaseSettings, Field

from ears import handlers
from ears.providers.deezer import DeezerProvider, DeezerSettings
from ears.types import Event


class Destinations(BaseSettings):
    broadcast: str = Field(..., env="DESTINATION_BROADCAST")


def on_broadcast_playlist_event(event: Event, _: Any) -> None:
    settings = DeezerSettings()
    provider = DeezerProvider(settings)
    destinations = Destinations()
    handlers.on_broadcast_playlist_event(
        provider,
        event,
        destinations.broadcast,
    )


def on_update_playlist_event(event: Event, _: Any) -> None:
    settings = DeezerSettings()
    provider = DeezerProvider(settings)
    handlers.on_update_playlist_event(provider, event)
