from ears.events import PlaylistAction, PlaylistEvent
from ears.messaging import publish
from ears.models import Resource, ResourceType

from router import CommandRequestPayload, CommandSyntaxError


def on_broadcast_command(payload: CommandRequestPayload) -> None:
    command = payload.text.split()
    if len(command) != 2:
        raise CommandSyntaxError(
            "broadcast *{provider}* *{playlist_id}*"
        )
    provider = command[0]
    playlist_id = command[1]
    event = PlaylistEvent(
        action=PlaylistAction.broadcast,
        playlist_urn=Resource(
            id=playlist_id,
            type=ResourceType.playlist,
            provider=provider,
            url=f"https://www.deezer.com/playlist/{playlist_id}"
        ),
    )
    publish(f"{provider}-broadcast-playlist", event)


def on_buy_command(payload: CommandRequestPayload) -> None:
    pass
