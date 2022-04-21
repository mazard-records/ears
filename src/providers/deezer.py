from typing import List

from httpx import Client

from ..models import Identifier, MusicEntity


class DeezerPlaylistView(object):
    pass


class Deezer(object):

    def __init__(self) -> None:
        self._transport = Client()

    def playlist(self, idenfitier: Identifier) -> List[DeezerPlaylistView]:
        pass
