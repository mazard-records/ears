from typing import Any

from ears import handlers
from ears.providers.deezer import DeezerProvider, DeezerSettings
from ears.types import Event


def on_broadcast_playlist_event(event: Event, _: Any) -> None:
    settings = DeezerSettings()
    provider = DeezerProvider(settings)
    # TODO: update with target topic
    destination = ...
    handlers.on_broadcast_playlist_event(provider, event, destination)


def on_update_playlist_event(event: Event, _: Any) -> None:
    settings = DeezerSettings()
    provider = DeezerProvider(settings)
    handlers.on_update_playlist_event(provider, event)
