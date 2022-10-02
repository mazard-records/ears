from typing import List, Optional

from httpx import Client
from pydantic import AnyHttpUrl, BaseModel, BaseSettings, Field

from ..models import Resource, ResourceType, Track, TrackMetadata, TrackSearchQuery
from . import AbstractMusicProvider


class DeezerSettings(BaseSettings):
    access_token: str = Field(..., env="DEEZER_ACCESS_TOKEN")


class DeezerArtist(BaseModel):
    name: str


class DeezerAlbum(BaseModel):
    cover: AnyHttpUrl
    title: str


class DeezerTrack(BaseModel):
    artist: DeezerArtist
    album: DeezerAlbum
    id: int
    link: str
    preview: AnyHttpUrl
    title: str

    def to_resource(self) -> Resource:
        return Resource(
            id=self.id,
            provider="deezer",
            url=self.link,
            type=ResourceType.track,
        )

    def to_track_metadata(self) -> TrackMetadata:
        return TrackMetadata(
            album=self.album.title,
            artist=self.artist.name,
            title=self.title,
            cover=self.album.cover,
            preview=self.preview,
        )

    def to_track(self) -> Track:
        return Track(
            metadata=self.to_track_metadata(),
            resource=self.to_resource(),
        )


class DeezerPlaylistTracks(BaseModel):
    data: List[DeezerTrack]


class DeezerPlaylist(BaseModel):
    tracks: DeezerPlaylistTracks


class DeezerProvider(AbstractMusicProvider):

    URL = "https://api.deezer.com"

    def __init__(self, settings: DeezerSettings) -> None:
        self._transport = Client(base_url=self.URL)
        self._access_token = settings.access_token

    def _url(self, path: str) -> str:
        return f"{path}?access_token={self._access_token}"

    @property
    def name(self) -> str:
        return "deezer"

    def get_playlist(
        self,
        playlist_urn: str,
    ) -> List[Track]:
        playlist = self.parse_urn(playlist_urn)
        endpoint = self._url(f"/playlist/{playlist.id}")
        response = self._transport.get(endpoint)
        response.raise_for_status()
        results = DeezerPlaylist(**response.json())
        return [result.to_track() for result in results.tracks.data]

    def add_to_playlist(
        self,
        playlist_urn: str,
        track_urn: Optional[str],
    ) -> None:
        playlist = self.parse_urn(playlist_urn)
        track = self.parse_urn(track_urn)
        endpoint = self._url(f"/playlist/{playlist.id}/tracks")
        endpoint = f"{endpoint}&songs={track.id}"
        response = self._transport.post(endpoint)
        response.raise_for_status()

    def remove_from_playlist(
        self,
        playlist_urn: str,
        track_urn: Optional[str],
    ) -> None:
        playlist = self.parse_urn(playlist_urn)
        track = self.parse_urn(track_urn)
        endpoint = self._url(f"/playlist/{playlist.id}/tracks")
        endpoint = f"{endpoint}&songs={track.id}"
        response = self._transport.delete(endpoint)
        response.raise_for_status()

    def search(
        self,
        query: TrackSearchQuery,
    ) -> List[Track]:
        raise NotImplementedError()
