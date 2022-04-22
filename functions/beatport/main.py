from base64 import b64decode
from json import loads
from typing import Any, Dict

from pydantic import BaseModel, BaseSettings

from transport import BeatportTransport


class WantlistSettings(BaseSettings):
    wantlist: int


class WantlistQuery(BaseModel):
    artist: str
    album: str
    name: str

    @classmethod
    def from_event(cls, event: Dict[str, Any]) -> "WantlistQuery":
        if "data" not in event:
            raise ValueError("Missing event data")
        return cls(**loads(b64decode(event["data"]).decode("utf-8")))


def entrypoint(event: Dict[str, Any], _: Any) -> None:
    # TODO: add complex error handling.
    settings = WantlistSettings()
    query = WantlistQuery.from_event(event)
    transport = BeatportTransport()
    transport.login()
    tracks = transport.search(query.artist, query.name)
    if len(tracks) == 0:
        # TODO: notify
        pass
    else:
        transport.add_track_to_playlist(
            settings.wantlist,
            [tracks[0].id],
        )
