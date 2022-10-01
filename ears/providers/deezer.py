from typing import List

from httpx import Client

from . import AbstractTrackProvider
from ..models import Track, TrackSearchQuery


class DeezerProvider(AbstractTrackProvider):

    URL = "https://api.deezer.com"

    def __init__(self, access_token: str) -> None:
        self._transport = Client(base_url=self.URL)
        self._access_token = access_token

    def _url(self, path: str) -> str:
        return f"{path}?access_token={self._access_token}"

    def add_to_playlist(
        self,
        playlist_urn: str,
        track_urn: str,
    ) -> None:
        track = self.parse_urn(track_urn)
        playlist = self.parse_urn(playlist_urn)
        endpoint = self._url(f"/playlist/{playlist.id}/tracks")
        endpoint = f"{endpoint}&songs={track.id}"
        response = self._transport.port(endpoint)
        response.raise_for_status()

    def remove_from_playlist(
        self,
        playlist_urn: str,
        track_urn: str,
    ) -> None:
        track = self.parse_urn(track_urn)
        playlist = self.parse_urn(playlist_urn)
        endpoint = self._url(f"/playlist/{playlist.id}/tracks")
        endpoint = f"{endpoint}&songs={track.id}"
        response = self._transport.delete(endpoint)
        response.raise_for_status()

    def search(query: TrackSearchQuery) -> List[Track]:
        # NOTE: we don't need search from Deezer provider.
        return []
