from abc import ABC, abstractproperty
from typing import Any, Callable, List
from urllib.parse import urlencode

from httpx import Client    

from ._models import TrackSearch
from ._settings import LoginSettings


AnyCallable = Callable[..., Any]


def trace(name: str) -> AnyCallable:
    def decorator(method: AnyCallable) -> AnyCallable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return method(*args, **kwargs)
            except Exception as e:
                # NOTE: log to stdout, consider adding JSON log
                #       with complex tracing.
                print(f"{name} - {e}")
                raise
        return wrapper
    return decorator


class TransportProvider(ABC):
    @abstractproperty
    def transport(self) -> Client:
        pass


class AuthorizationTransportMixin(TransportProvider):
    """ Transport mixin that provides authorization process. """

    @trace("AuthorizationTransportMixin#login")
    def login(self) -> None:
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
        settings = LoginSettings()
        # NOTE: perform login call and check for errors.
        response = self._transport.post(
            "/api/account/login",
            headers=headers,
            json=settings.dict()
        )
        response.raise_for_status()


class SearchTransportMixin(TransportProvider):
    """ Transport mixin that provides track Search feature from transport. """

    @trace("SearchTransportMixin#search")
    def search(self, artist: str, track: str) -> List[TrackSearch]:
        query = (
            "type=tracks"
            f"&q={urlencode(track)}"
            f"&artist_name={urlencode(artist)}"
        )
        response = self._transport.get(f"/api/v4/catalog/search?{query}")
        response.raise_for_status()
        return TrackSearch(**response.json())


class PlaylistTransportMixin(object):
    """ Transport mixin for interacting with a playlist. """
    
    @trace("PlaylistTransportMixin#add_track_to_playlist")
    def add_track_to_playlist(self, playlist_id: int, tracks: List[int]) -> None:
        endpoint = f"/v4/my/playlists/{playlist_id}/tracks/bulk"
        payload = {"track_ids": tracks}
        response = self._transport.post(endpoint, json=payload)
        response.raise_for_status()

