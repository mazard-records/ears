from typing import List
from urllib.parse import quote

from httpx import Client
from pydantic import BaseSettings

from models import SearchQuery, TrackSearch

class LoginSettings(BaseSettings):
    username: str
    password: str
    remember: bool = False


class BeatportTransport(object):

    URL = "https://www.beatport.com"
    USER_AGENT =  (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/15.1 Safari/605.1.15"
    )

    def __init__(self) -> None:
        self._transport = Client(
            base_url=self.URL,
            headers={
                "User-Agent": self.USER_AGENT,
                "Origin": self.URL,
                "Referer": f"{self.URL}/",
            },
        )

    @property
    def transport(self) -> Client:
        return self._transport

    def add_track_to_playlist(self, playlist_id: int, tracks: List[int]) -> None:
        endpoint = f"/api/v4/my/playlists/{playlist_id}/tracks/bulk"
        payload = {"track_ids": tracks}
        response = self._transport.post(endpoint, json=payload)
        response.raise_for_status()

    def login(self, username: str, password: str) -> None:
        # NOTE: perform some prior call to fill cookies
        #       and get a valid CSRF token.
        self.transport.get("/api/my-beatport")
        self.transport.get("/api/account")
        self.transport.get("/api/csrfcheck")
        # NOTE: Build payload and headers.
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-GB,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": self._transport.cookies.get("_csrf_token"),
        }
        # NOTE: perform login call and check for errors.
        response = self._transport.post(
            "/api/account/login",
            headers=headers,
            json={
                "username": username,
                "password": password,
                "remember": False,
            }
        )
        response.raise_for_status()

    def search(self, query: SearchQuery) -> List[TrackSearch]:
        query = (
            f"q={quote(query.title)}"
            f"&artist_name={quote(query.artist)}"
            "&type=tracks"
        )
        response = self._transport.get(f"/api/v4/catalog/search?{query}")
        response.raise_for_status()
        return TrackSearch(**response.json())
