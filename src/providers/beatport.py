from typing import Dict, List, Union
from urllib.parse import urlencode

from httpx import Client

from tests.beatport import LoginPayload

from ..models.beatport import LoginPayload, TrackSearch

_BeatportAPIHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
}

_BeatportURL = "https://www.beatport.com"
_BeatportUserAgent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/15.1 Safari/605.1.15"
)

class BeatportPlaylistView(object):

    def __init__(self, transport: Client, playlist_id: int) -> None:
        self._id = playlist_id
        self._transport = transport
    
    def add(self, tracks: List[int]) -> None:
        endpoint = f"/v4/my/playlists/{self._id}/tracks/bulk"
        payload = {"track_ids": tracks}
        response = self._transport.post(endpoint, json=payload)
        response.raise_for_status()


class BeatportProvider(object):

    def __init__(self) -> None:
        self._transport = Client(
            base_url=_BeatportURL,
            headers={
                "User-Agent": _BeatportUserAgent,
                "Origin": _BeatportURL,
                "Referer": "https://www.beatport.com/",
            },
        )

    def login(self, username: str, password: str) -> None:
        # NOTE: perform some prior call to fill cookies
        #       and get a valid CSRF token.
        self._transport.get("/api/my-beatport")
        self._transport.get("/api/account")
        self._transport.get("/api/csrfcheck")
        # NOTE: Build payload and headers.
        headers = {
            "X-CSRFToken": self._transport.cookies.get("_csrf_token"),
        } | _BeatportAPIHeaders
        payload = LoginPayload(username=username, password=password)
        # NOTE: perform login call and check for errors.
        response = self._transport.post(
            "/api/account/login",
            headers=headers,
            json=payload.dict()
        )
        response.raise_for_status()

    def search(self, artist: str, track: str) -> List[TrackSearch]:
        query = (
            "type=tracks"
            f"&q={urlencode(track)}"
            f"&artist_name={urlencode(artist)}"
        )
        response = self._transport.get(f"/api/v4/catalog/search?{query}")
        response.raise_for_status()
        return TrackSearch(**response.json())

    def playlist(self, name_or_int: Union[int, str]) -> BeatportPlaylistView:
        if isinstance(name_or_int, int):
            playlist_id = name_or_int
        else:
            # TODO: search playlist, match by name
            playlist_id = ...
            raise NotImplementedError()
        return BeatportPlaylistView(self._transport, playlist_id)