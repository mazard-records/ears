import json

from base64 import b64decode
from enum import Enum
from typing import Any, Dict

from pydantic import AnyHttpUrl, BaseModel


class Provider(str, Enum):
    beatport = "beatport"


class MatchingSource(BaseModel):
    identifier: Any
    provider: str
    url: AnyHttpUrl

    def to_urn(self) -> str:
        return f"urn:{self.provider}:{self.identifier}"


class MatchingTrack(BaseModel):
    origin: MatchingSource
    destination: MatchingSource
    provider: Provider
    album: str
    artist: str
    title: str
    cover: AnyHttpUrl

    @classmethod
    def from_event(cls, event: Dict[str, Any]) -> "MatchingTrack":
        if "data" not in event:
            raise ValueError("Missing matching event data")
        return cls(**json.loads(b64decode(event["data"]).decode("utf-8")))

    def to_markdown_link(self) -> str:
        return f"*<{self.destination.url}|{self.title} - {self.artist}>*"

    def to_uri(self, action: str) -> str:
        return (
            f"ears://matching/{action}"
            f"/{self.origin.to_urn()}"
            f"/{self.destination.to_urn()}"
        )
