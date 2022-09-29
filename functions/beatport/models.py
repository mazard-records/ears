from typing import Any, Dict, List, Optional

from pydantic import AnyHttpUrl, BaseModel


class Identifiable(BaseModel):
    id: int


class Named(Identifiable):
    name: str


class Artist(Named):
    slug: str
    url: str


class Image(Identifiable):
    uri: AnyHttpUrl


class Release(Named):
    image: Image


class Track(Named):
    artists: List[Artist]
    image: Image
    mix_name: str
    release: Release
    sample_url: AnyHttpUrl


class TrackSearch(BaseModel):
    count: int
    page: str
    per_page: int
    next: Optional[str]
    previous: Optional[str]
    tracks: List[Track]


class SearchQuery(BaseModel):
    artist: str
    title: str