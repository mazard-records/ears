from base64 import b64encode
from unittest.mock import Mock

from pytest_mock import MockerFixture

from ears.events import PlaylistAction, PlaylistEvent
from ears.handlers import (
    on_broadcast_playlist_event,
    on_search_event,
    on_update_playlist_event,
)
from ears.models import (
    Resource,
    ResourceType,
    Track,
    TrackMatching,
    TrackMetadata,
    TrackSearchQuery,
)
from ears.types import Event, PydanticModel

_FRENCH_CRUSH = Track(
    metadata=TrackMetadata(
        album="Delighted",
        artist="Herr Krank",
        title="French crush",
        cover="https://ears.com/cover.png",
        preview="https://ears.com/preview.mp3",
    ),
    resource=Resource(
        id=69,
        provider="ears",
        type="track",
        url="https://ears.com/69",
    ),
)

_FRENCH_CRUSH_DATA = _FRENCH_CRUSH.json().encode("utf-8")
_PLAYLIST_URN = "urn:ears:playlist:51"
_TRACK_URN = "urn:ears:track:69"


def pydantic_model_to_event(model: PydanticModel) -> Event:
    return {"data": b64encode(model.json().encode("utf-8"))}


def test_on_broadcast_playlist_event(
    mocker: MockerFixture,
    publisher_mock: Mock,
) -> None:
    event = pydantic_model_to_event(
        PlaylistEvent(
            action=PlaylistAction.broadcast,
            playlist_urn=_PLAYLIST_URN,
        )
    )
    provider = mocker.MagicMock()
    provider.get_playlist = mocker.Mock(return_value=[_FRENCH_CRUSH])
    on_broadcast_playlist_event(provider, event, "broadcast_playlist")
    provider.get_playlist.assert_called_once_with(_PLAYLIST_URN)
    publisher_mock.assert_called_once_with(
        f"projects/ears/topics/broadcast_playlist",
        _FRENCH_CRUSH_DATA,
    )


def test_on_update_playlist_event(mocker: MockerFixture) -> None:
    provider = mocker.MagicMock()
    provider.add_to_playlist = mocker.Mock()
    provider.remove_from_playlist = mocker.Mock()
    event_add = pydantic_model_to_event(
        PlaylistEvent(
            action=PlaylistAction.add,
            playlist_urn=_PLAYLIST_URN,
            track_urn=_TRACK_URN,
        )
    )
    event_remove = pydantic_model_to_event(
        PlaylistEvent(
            action=PlaylistAction.remove,
            playlist_urn=_PLAYLIST_URN,
            track_urn=_TRACK_URN,
        )
    )
    on_update_playlist_event(provider, event_add)
    provider.add_to_playlist.assert_called_once_with(
        _PLAYLIST_URN,
        _TRACK_URN,
    )
    on_update_playlist_event(provider, event_remove)
    provider.remove_from_playlist.assert_called_once_with(
        _PLAYLIST_URN,
        _TRACK_URN,
    )


def test_on_search_event(
    mocker: MockerFixture,
    publisher_mock: Mock,
) -> None:
    event = pydantic_model_to_event(_FRENCH_CRUSH)
    provider = mocker.MagicMock()
    provider.search = mocker.Mock(return_value=[_FRENCH_CRUSH])
    on_search_event(provider, event, "search")
    provider.search.assert_called_once_with(_FRENCH_CRUSH.metadata)
    publisher_mock.assert_called_once_with(
        f"projects/ears/topics/search",
        TrackMatching(
            origin=_FRENCH_CRUSH.resource,
            destination=_FRENCH_CRUSH.resource,
            metadata=_FRENCH_CRUSH.metadata,
        )
        .json()
        .encode("utf-8"),
    )
