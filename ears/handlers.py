from flask import Request, Response, jsonify

from .providers import AbstractMusicProvider
from .models import Resource, TrackSearchQuery
from .types import DomainHandler


def on_matching_action(path: str) -> Optional[str]:
    """
    Domain handler for InteractionRouter which acknowledge matching
    action and publish a message into a Pub/Sub topic accordingly.
    """
    tokens = url.split("/")
    # NOTE: url start with / so we have an empty token.
    if len(tokens) != 4:
        raise ValueError("Invalid matching URL")
    action = tokens[1]
    origin = MatchingSource.from_urn(tokens[2])
    destination = MatchingSource.from_urn(tokens[3])
    producer = MessageProducer(destination.provider)
    if action == "validate":
        producer({"id": destination.identifier})
    elif action == "invalidate":
        logging.debug(
            f"Deny matching {origin.provider}#{origin.identifier}"
            f" -> {destination.provider}#{destination.identifier}"
        )
    else:
        raise ValueError("Invalid action")


def on_get_playlist_request(
    provider: AbstractMusicProvider,
    request: Request,
) -> Response:
    playlist = Resource(**request.get_json())
    tracks = provider.get_playlist(playlist.to_urn())
    return jsonify([track.dict() for track in tracks])


def on_add_to_playlist_request(
    provider: AbstractMusicProvider,
    request: Request,
) -> Response:
    return jsonify(None)


def on_remove_from_playlist_request(
    provider: AbstractMusicProvider,
    request: Request,
) -> Response:
    return jsonify(None)


def on_search_request(
    provider: AbstractMusicProvider,
    request: Request,
) -> Response:
    query = TrackSearchQuery(**request.get_json())
    tracks = provider.search(query)
    if len(tracks) == 0:
        return jsonify(None)
    return jsonify(tracks[0].dict())
