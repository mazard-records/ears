
from typer import run

from .models import Identifier
from .providers.deezer import Deezer


def entrypoint(
    wantlist_id: Identifier,
    sink: Identifier,
) -> None:
    deezer = Deezer()
    providers = []  # Add beatport, then bandcamp
    wantlist = deezer.playlist("wantlist_id")
    sink = deezer.playlist("sink_id")
    for track in wantlist:
        for provider in providers:

