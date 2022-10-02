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

    @classmethod
    def from_urn(cls, urn: Optional[str]) -> "Resource":
        """
        Parse the given URN into a target TrackSource.
        Such URN are designed as follow:

        urn:PROVIDER:TYPE:IDENTIFIER

        Where given provider should match this object target.
        """
        if urn is None:
            raise ValueError()
        tokens = urn.split(":")
        if len(tokens) != 4 or tokens[0] != "urn":
            raise ValueError(f"Invalid urn {urn}")
        return Resource(
            id=tokens[3],
            provider=tokens[1],
            type=tokens[2],
        )

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
    metadata: Optional[TrackMetadata] = None


class TrackSearchQuery(BaseModel):
    album: Optional[str] = None
    artist: str
    title: str
