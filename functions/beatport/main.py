from base64 import b64decode
from json import loads
from typing import Any, Dict

from flask import Request, Response, jsonify
from pydantic import BaseModel, BaseSettings, Field

from models import SearchQuery
from transport import BeatportTransport


class Settings(BaseSettings):
    username: str = Field(..., env="USERNAME")
    password: str = Field(..., env="PASSWORD")
    wantlist: int = Field(..., env="WANTLIST")

    class Config:
        env_previx = "BEATPORT_"


class WantlistQuery(BaseModel):
    artist: str
    album: str
    name: str

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
        return jsonify({})
    return jsonify(results.tracks[0])


def on_wantlist_event(event: Dict[str, Any], _: Any) -> None:
    settings = Settings()
    transport = BeatportTransport()
    transport.login(settings.username, settings.password)
