from enum import Enum
from typing import Any, Optional

from pydantic import AnyHttpUrl, BaseModel


class ResourceType(str, Enum):
    playlist = "playlist"
    track = "track"


class Resource(BaseModel):
    id: Any
    provider: str
    type: ResourceType
    url: Optional[AnyHttpUrl] = None

    def to_urn(self) -> str:
        return f"urn:{self.provider}:{self.type}:{self.id}"


class TrackMetadata(BaseModel):
    album: str
    artist: str
    title: str
    cover: AnyHttpUrl
    preview: Optional[AnyHttpUrl] = None


class Track(BaseModel):
    metadata: TrackMetadata
    resource: Resource


class TrackMatching(BaseModel):
    origin: Resource
    destination: Resource
    metadata: TrackMetadata


class TrackSearchQuery(BaseModel):
    album: Optional[str] = None
    artist: str
    title: str
