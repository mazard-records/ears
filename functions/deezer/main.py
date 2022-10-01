from flask import Request, Response

from ears.handlers import on_get_playlist_request
from ears.providers.deezer import DeezerProvider


def get_playlist(request: Request) -> Response:
    on_get_playlist_request(
        DeezerProvider(access_token=...),
        request,
    )
