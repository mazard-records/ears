from ears.providers.deezer import DeezerProvider, DeezerSettings
from pytest import fixture
from pytest_httpx import HTTPXMock


@fixture(scope="session")
def deezer_provider() -> None:
    settings = DeezerSettings(access_token="token")
    provider = DeezerProvider(settings)
    return provider


_PLAYLIST_ENDPOINT = (
    "https://api.deezer.com"
    "/playlist"
    "/666"
    "/tracks?access_token=token&songs=42"
)
_PLAYLIST_URN = "urn:deezer:666"
_TRACK_URN = "urn:deezer:42"


def test_get_playlist(
    deezer_provider: DeezerProvider,
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(
        url="https://api.deezer.com/playlist/666?access_token=token",
        method="GET",
        json={
            "tracks": {
                "data": [
                    {
                        "id": 42,
                        "title": "San",
                        "link": "https://deezer.com/track/42",
                        "preview": "https://deezer.com/track/42/preview",
                        "artist": {
                            "name": "Orelsan",
                        },
                        "album": {
                            "title": "La fete est finie",
                            "cover": "https://deezer.com/track/42/preview",
                        }
                    }
                ]
            }
    })
    tracks = deezer_provider.get_playlist(_PLAYLIST_URN)
    assert len(tracks) == 1
    assert tracks[0].resource.id == 42
    assert tracks[0].resource.provider == "deezer"
    assert tracks[0].resource.url == "https://deezer.com/track/42"
    assert tracks[0].metadata.album == "La fete est finie"
    assert tracks[0].metadata.artist == "Orelsan"
    assert tracks[0].metadata.title == "San"
    assert tracks[0].metadata.cover == "https://deezer.com/track/42/preview"
    assert tracks[0].metadata.preview == "https://deezer.com/track/42/preview"


def test_add_to_playlist(
    deezer_provider: DeezerProvider,
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(
        url=_PLAYLIST_ENDPOINT,
        method="POST",
    )
    deezer_provider.add_to_playlist(_PLAYLIST_URN, _TRACK_URN)
    requests = httpx_mock.get_requests(
        url=_PLAYLIST_ENDPOINT,
        method="POST",
    )
    assert len(requests) == 1


def test_remove_from_playlist(
    deezer_provider: DeezerProvider,
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(
        url=_PLAYLIST_ENDPOINT,
        method="DELETE",
    )
    deezer_provider.remove_from_playlist(_PLAYLIST_URN, _TRACK_URN)
    requests = httpx_mock.get_requests(
        url=_PLAYLIST_ENDPOINT,
        method="DELETE",
    )
    assert len(requests) == 1
