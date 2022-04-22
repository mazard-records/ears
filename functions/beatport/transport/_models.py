from typing import List, Optional
from pydantic import BaseModel


class Artist(BaseModel):
    id: int
    name: str
    slug: str
    url: str


class Track(BaseModel):
    artists: List[Artist]
    id: int
    name: str
    mix_name: str


class TrackSearch(BaseModel):
    count: int
    page: str
    per_page: int
    next: Optional[str]
    previous: Optional[str]
    tracks: List[Track]
