from base64 import b64decode
from functools import lru_cache
from json import loads
from typing import Any, Dict

from flask import Request, Response, jsonify
from pydantic import BaseModel, BaseSettings, Field, validator

from models import SearchQuery
from transport import BeatportTransport


class _Settings(BaseSettings):
    username: str = Field(..., env="BEATPORT_USERNAME")
    password: str = Field(..., env="BEATPORT_PASSWORD")
    wantlist: int = Field(..., env="BEATPORT_WANTLIST")


@lru_cache(maxsize=1)
def Settings() -> _Settings:
    return _Settings()


@lru_cache(maxsize=1)
def AuthenticatedTransport() -> BeatportTransport:
    settings = Settings()
    transport = BeatportTransport()
    transport.login(settings.username, settings.password)
    return transport


class WantlistQuery(BaseModel):
    id: int

    @validator("id", pre=True)
    def validate_id(cls, value: Any) -> int:
        return int(value)

    @classmethod
    def from_event(cls, event: Dict[str, Any]) -> "WantlistQuery":
        if "data" not in event:
            raise ValueError("Missing event data")
        return cls(**loads(b64decode(event["data"]).decode("utf-8")))


def on_search_request(request: Request) -> Response:
    transport = BeatportTransport()
    query = SearchQuery(**request.get_json())
    results = transport.search(query)
    if len(results.tracks) == 0:
        return jsonify(None)
    return jsonify(results.tracks[0].dict())


def on_wantlist_event(event: Dict[str, Any], _: Any) -> None:
    settings = Settings()
    query = WantlistQuery.from_event(event)
    transport = AuthenticatedTransport()
    transport.add_track_to_playlist(
        settings.wantlist,
        tracks=[query.id],
    )
