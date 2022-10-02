import json

from urllib.parse import quote
from ears.models import TrackSearchQuery

from ears.providers.beatport import BeatportProvider
from pytest import fixture
from pytest_httpx import HTTPXMock


@fixture(scope="session")
def beatport_provider() -> BeatportProvider:
    return BeatportProvider()

_API = "https://www.beatport.com/api/v4"
_PLAYLIST_ENDPOINT = (
    f"{_API}"
    "/my"
    "/playlists"
    "/666"
    "/tracks"
)
_PLAYLIST_URN = "urn:beatport:666"
_TRACK_URN = "urn:beatport:42"


def test_login(
    beatport_provider: BeatportProvider,
    httpx_mock: HTTPXMock,
) -> None:
    pass


def test_add_to_playlist(
    beatport_provider: BeatportProvider,
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(
        url=f"{_PLAYLIST_ENDPOINT}/bulk",
        method="POST",
    )
    beatport_provider.add_to_playlist(_PLAYLIST_URN, _TRACK_URN)
    requests = httpx_mock.get_requests(
        url=f"{_PLAYLIST_ENDPOINT}/bulk",
        method="POST",
    )
    assert len(requests) == 1
    payload = json.loads(requests[0].content.decode("utf-8"))
    assert "track_ids" in payload
    assert len(payload["track_ids"]) == 1
    assert payload["track_ids"][0] == 42


def test_remove_from_playlist(
    beatport_provider: BeatportProvider,
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(
        url=f"{_PLAYLIST_ENDPOINT}/42",
        method="DELETE",
    )
    beatport_provider.remove_from_playlist(_PLAYLIST_URN, _TRACK_URN)
    requests = httpx_mock.get_requests(
        url=f"{_PLAYLIST_ENDPOINT}/42",
        method="DELETE",
    )
    assert len(requests) == 1


def test_search(
    beatport_provider: BeatportProvider,
    httpx_mock: HTTPXMock,
) -> None:
    query = TrackSearchQuery(
        title="Off to paradise",
        artist="Demuja",
    )
    endpoint = (
        f"{_API}/catalog/search"
        "?type=tracks"
        f"q={quote(query.title)}"
        f"&artist_name={quote(query.artist)}"
    )
    httpx_mock.add_response(
        url=endpoint,
        method="GET",
        json={
            "tracks": [
                {
                    "id": 42,
                    "name": "Off to Paradise",
                    "artists": [
                        {
                            "id": 69,
                            "slug": "demuja",
                            "name": "Demuja",
                        },
                    ],
                    "image": {
                        "id": 51,
                        "uri": "https://demuja.png",
                    },
                    "mix_name": "Original mix",
                    "release": {
                        "id": 13,
                        "name": "Off to paradise"
                    },
                    "sample_url": "https://demuja.mp3",
                    "slug": "off-to-paradise",
                }
            ]
        }
    )
    tracks = beatport_provider.search(query)
    assert len(tracks) == 1
    assert tracks[0].resource.id == 42
    assert tracks[0].resource.provider == "beatport"
    assert tracks[0].resource.url == "https://www.beatport.com/track/off-to-paradise/42"
    assert tracks[0].metadata.album == "Off to paradise"
    assert tracks[0].metadata.artist == "Demuja"
    assert tracks[0].metadata.title == "Off to paradise"
    assert tracks[0].metadata.cover == "https://demuja.png"
    assert tracks[0].metadata.preview == "https://demuja.mp3"
