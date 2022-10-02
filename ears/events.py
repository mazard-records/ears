from enum import Enum
from typing import Optional

from pydantic import BaseModel


class PlaylistAction(str, Enum):
    add = "add"
    broadcast = "broadcast"
    remove = "remove"


class PlaylistEvent(BaseModel):
    playlist_urn: str
    track_urn: Optional[str] = None
    action: PlaylistAction
