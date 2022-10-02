from .events import PlaylistAction, PlaylistEvent
from .messaging import EventPublisher, pydantic_model_from_event
from .models import TrackSearchQuery
from .providers import AbstractMusicProvider
from .types import Event


def on_broadcast_playlist_event(
    provider: AbstractMusicProvider,
    event: Event,
    destination: str,
) -> None:
    playlist_event = pydantic_model_from_event(PlaylistEvent, event)
    tracks = provider.get_playlist(playlist_event.playlist_urn)
    publisher = EventPublisher(destination)
    for track in tracks:
        publisher(track)


def on_update_playlist_event(
    provider: AbstractMusicProvider,
    event: Event,
) -> None:
    playlist_event = pydantic_model_from_event(PlaylistEvent, event)
    if playlist_event.action == PlaylistAction.add:
        provider.add_to_playlist(
            playlist_event.playlist_urn,
            playlist_event.track_urn,
        )
    elif playlist_event.action == PlaylistAction.remove:
        provider.remove_from_playlist(
            playlist_event.playlist_urn,
            playlist_event.track_urn,
        )


def on_search_event(
    provider: AbstractMusicProvider,
    event: Event,
    destination: str,
) -> None:
    query = pydantic_model_from_event(TrackSearchQuery, event)
    results = provider.search(query)
    if len(results) == 0:
        # TODO: figure out what to do here.
        return
    publisher = EventPublisher(destination)
    publisher(results[0])
