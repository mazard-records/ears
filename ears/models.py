from enum import Enum
from typing import Any, Optional

from pydantic import AnyHttpUrl, BaseModel


class Resource(BaseModel):
    id: Any
    provider: str
    url: Optional[AnyHttpUrl] = None

    def to_urn(self) -> str:
        return f"urn:{self.provider}:{self.id}"


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

    def to_url(self) -> str:
        path = "/".join([
            "matching",
            self.origin.to_urn(),
            self.destination.to_urn(),
        ])
        return f"ears://{path}"


class TrackSearchQuery(BaseModel):
    album: Optional[str] = None
    artist: str
    title: str
