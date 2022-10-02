from typing import Any, Dict, List, Optional
from urllib.parse import quote

from httpx import Client
from pydantic import AnyHttpUrl, BaseModel, BaseSettings, Field

from ..models import Resource, ResourceType, Track, TrackMetadata, TrackSearchQuery
from . import AbstractMusicProvider


class BeatportIdentifiableResource(BaseModel):
    id: int


class BeatportNamedResource(BeatportIdentifiableResource):
    name: str


class BeatportArtist(BeatportNamedResource):
    slug: str
    url: str


class BeatportImage(BeatportIdentifiableResource):
    uri: AnyHttpUrl


class Release(BeatportNamedResource):
    image: BeatportImage


class BeatportTrack(BeatportNamedResource):
    artists: List[BeatportArtist]
    image: BeatportImage
    mix_name: str
    release: Release
    sample_url: AnyHttpUrl
    slug: str

    def to_resource(self) -> Resource:
        return Resource(
            id=self.id,
            provider="beatport",
            url=f"https://www.beatport.com/track/{self.slug}/{self.id}",
            type=ResourceType.track,
        )

    def to_track_metadata(self) -> TrackMetadata:
        if len(self.artists) == 0:
            artist = "Unknown"
        else:
            artist = self.artists[0].name
        return TrackMetadata(
            album=self.release.name,
            artist=artist,
            title=self.name,
            cover=self.image.uri,
            preview=self.sample_url,
        )

    def to_track(self) -> Track:
        return Track(
            metadata=self.to_track_metadata(),
            resource=self.to_resource(),
        )


class BeatportTrackSearchResult(BaseModel):
    tracks: List[BeatportTrack]


class BeatportLoginSettings(BaseSettings):
    username: str = Field(..., env="BEATPORT_USERNAME")
    password: str = Field(..., env="BEATPORT_PASSWORD")
    remember: bool = False


class BeatportProvider(AbstractMusicProvider):

    LOGIN_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-GB,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
    }

    URL = "https://www.beatport.com"

    USER_AGENT = (
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
    def name(self) -> str:
        return "beatport"

    def login(
        self,
        settings: BeatportLoginSettings,
    ) -> None:
        # NOTE: perform some prior call to fill cookies
        #       and get a valid CSRF token.
        self._transport.get("/api/my-beatport")
        self._transport.get("/api/account")
        self._transport.get("/api/csrfcheck")
        csrf_token = self._transport.cookies.get("_csrf_token")
        headers = self.LOGIN_HEADERS.copy()
        if csrf_token is None:
            raise ValueError("Missing CSRF token")
        headers["X-CSRFToken"] = csrf_token
        response = self._transport.post(
            "/api/account/login", headers=headers, json=settings.dict()
        )
        response.raise_for_status()

    def get_playlist(
        self,
        playlist_urn: str,
    ) -> List[Track]:
        raise NotImplementedError()

    def add_to_playlist(
        self,
        playlist_urn: str,
        track_urn: Optional[str],
    ) -> None:
        playlist = self.parse_urn(playlist_urn)
        track = self.parse_urn(track_urn)
        endpoint = f"/api/v4/my/playlists/{playlist.id}/tracks/bulk"
        payload = {"track_ids": [track.id]}
        response = self._transport.post(endpoint, json=payload)
        response.raise_for_status()

    def remove_from_playlist(
        self,
        playlist_urn: str,
        track_urn: Optional[str],
    ) -> None:
        playlist = self.parse_urn(playlist_urn)
        track = self.parse_urn(track_urn)
        endpoint = f"/api/v4/my/playlists/{playlist.id}/tracks/{track.id}"
        response = self._transport.delete(endpoint)
        response.raise_for_status()

    def search(
        self,
        query: TrackSearchQuery,
    ) -> List[Track]:
        endpoint = (
            "/api/v4/catalog/search"
            "?type=tracks"
            f"q={quote(query.title)}"
            f"&artist_name={quote(query.artist)}"
        )
        response = self._transport.get(endpoint)
        response.raise_for_status()
        results = BeatportTrackSearchResult(**response.json())
        return [result.to_track() for result in results.tracks]
