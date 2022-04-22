

from typing import Any, Dict
from base64 import b64decode
from json import loads
from typing import Any, Dict

from pydantic import BaseModel

from transport import BeatportTransport


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
    # TODO: add error handling.
    query = WantlistQuery.from_event(event)
    transport = BeatportTransport()
    transport.login()
    tracks = transport.search(query.artist, query.name)
    if len(tracks) == 0:
        # TODO: notify
        pass
    else:
        # TODO: fetch playlist_id
        transport.add_track_to_playlist(..., [tracks[0].id])
        