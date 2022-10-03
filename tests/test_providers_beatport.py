import json
from urllib.parse import quote

from pytest_httpx import HTTPXMock

from ears.models import ResourceType, TrackSearchQuery
from ears.providers.beatport import BeatportLoginSettings, BeatportProvider

_API = "https://www.beatport.com/api/v4"
_PLAYLIST_ENDPOINT = f"{_API}" "/my" "/playlists" "/666" "/tracks"
_PLAYLIST_URN = "urn:beatport:playlist:666"
_TRACK_URN = "urn:beatport:track:42"

_LOGIN_PRIORS = ("my-beatport", "account", "csrfcheck")


def test_login(httpx_mock: HTTPXMock) -> None:
    for prior in _LOGIN_PRIORS:
        httpx_mock.add_response(
            method="GET",
            url=f"https://www.beatport.com/api/{prior}",
        )
    httpx_mock.add_response(
        method="POST",
        url="https://www.beatport.com/api/account/login",
    )
    settings = BeatportLoginSettings(username="Faylixe", password="You wish")
    provider = BeatportProvider()
    provider._transport.cookies.update({"_csrf_token": "hack"})
    provider.login(settings)
    for prior in _LOGIN_PRIORS:
        requests = httpx_mock.get_requests(
            url=f"https://www.beatport.com/api/{prior}",
            method="GET",
        )
        assert len(requests) == 1
    requests = httpx_mock.get_requests(
        method="POST",
        url="https://www.beatport.com/api/account/login",
    )
    assert len(requests) == 1
    assert requests[0].headers.get("X-CSRFToken") == "hack"
    payload = json.loads(requests[0].content.decode("utf-8"))
    assert payload.get("username") == "Faylixe"
    assert payload.get("password") == "You wish"
    assert payload.get("remember") == False


def test_add_to_playlist(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=f"{_PLAYLIST_ENDPOINT}/bulk",
        method="POST",
    )
    provider = BeatportProvider()
    provider.add_to_playlist(_PLAYLIST_URN, _TRACK_URN)
    requests = httpx_mock.get_requests(
        url=f"{_PLAYLIST_ENDPOINT}/bulk",
        method="POST",
    )
    assert len(requests) == 1
    payload = json.loads(requests[0].content.decode("utf-8"))
    assert "track_ids" in payload
    assert len(payload["track_ids"]) == 1
    assert payload["track_ids"][0] == "42"


def test_remove_from_playlist(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=f"{_PLAYLIST_ENDPOINT}/42",
        method="DELETE",
    )
    provider = BeatportProvider()
    provider.remove_from_playlist(_PLAYLIST_URN, _TRACK_URN)
    requests = httpx_mock.get_requests(
        url=f"{_PLAYLIST_ENDPOINT}/42",
        method="DELETE",
    )
    assert len(requests) == 1


def test_search(httpx_mock: HTTPXMock) -> None:
    query = TrackSearchQuery(
        album="Off to paradise",
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
                    "name": "Off to paradise",
                    "artists": [
                        {
                            "id": 69,
                            "slug": "demuja",
                            "name": "Demuja",
                            "url": "https://demuja.io",
                        },
                    ],
                    "image": {
                        "id": 51,
                        "uri": "https://demuja.png",
                    },
                    "mix_name": "Original mix",
                    "release": {
                        "id": 13,
                        "name": "Off to paradise",
                        "image": {
                            "id": 51,
                            "uri": "https://demuja.png",
                        },
                    },
                    "sample_url": "https://demuja.mp3",
                    "slug": "off-to-paradise",
                }
            ]
        },
    )
    provider = BeatportProvider()
    tracks = provider.search(query)
    assert len(tracks) == 1
    assert tracks[0].resource.id == 42
    assert tracks[0].resource.provider == "beatport"
    assert tracks[0].resource.url == "https://www.beatport.com/track/off-to-paradise/42"
    assert tracks[0].resource.type == ResourceType.track
    assert tracks[0].metadata.album == "Off to paradise"
    assert tracks[0].metadata.artist == "Demuja"
    assert tracks[0].metadata.title == "Off to paradise"
    assert tracks[0].metadata.cover == "https://demuja.png"
    assert tracks[0].metadata.preview == "https://demuja.mp3"
