from pydantic import BaseModel

from .models import TrackSource


class EARSProtocol(object):
    """ Stateless namespace of utilities that designing EARS protocol. """

    SCHEME = "ears"
    """ Protocol scheme. """

    def parse_urn(self, urn: str) -> TrackSource:
        """
        Parse the given URN into a target TrackSource.
        Such URN are designed as follow:

        urn:PROVIDER:IDENTIFIER

        Where provider should match any of the supported
        ._models.TrackProvider enum.
        """
        tokens = urn.split(":")
        if len(tokens) != 3 or tokens[0] != "urn":
            raise ValueError(f"Invalid urn {urn}")
        # TODO: check provider.
        return TrackSource(
            identifier=tokens[2],
            provider=tokens[1],
        )

    def to_urn(self, source: TrackSource) -> str:
        return f"urn:{source.provider}:{source.identifier}"
