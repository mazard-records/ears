from typing import Any

from ears import handlers
from ears.providers.beatport import BeatportLoginSettings, BeatportProvider
from ears.types import Event


def on_update_playlist_event(event: Event, _: Any) -> None:
    settings = BeatportLoginSettings()
    provider = BeatportProvider()
    provider.login(settings)
    handlers.on_update_playlist_event(provider, event)


def on_search_event(event: Event, _: Any) -> None:
    provider = BeatportProvider()
    # TODO: update with target topic
    destination = ...
    handlers.on_search_event(provider, event, destination)
