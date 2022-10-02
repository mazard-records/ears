from abc import ABC, abstractmethod, abstractproperty
from typing import List, Optional

from ..models import Resource, Track, TrackSearchQuery


class AbstractMusicProvider(ABC):
    """
    A music provi
    """

    @abstractproperty
    def name(self) -> str:
        pass

    @abstractmethod
    def get_playlist(
        self,
        playlist_urn: str,
    ) -> List[Track]:
        pass

    @abstractmethod
    def add_to_playlist(
        self,
        playlist_urn: str,
        track_urn: Optional[str],
    ) -> None:
        pass

    @abstractmethod
    def remove_from_playlist(
        self,
        playlist_urn: str,
        track_urn: Optional[str],
    ) -> None:
        pass

    @abstractmethod
    def search(
        self,
        query: TrackSearchQuery,
    ) -> List[Track]:
        pass

    def parse_urn(self, urn: Optional[str]) -> Resource:
        """
        Parse the given URN into a target TrackSource.
        Such URN are designed as follow:

        urn:PROVIDER:TYPE:IDENTIFIER

        Where given provider should match this object target.
        """
        if urn is None:
            raise ValueError()
        tokens = urn.split(":")
        if len(tokens) != 4 or tokens[0] != "urn":
            raise ValueError(f"Invalid urn {urn}")
        if tokens[1] != self.name:
            raise ValueError(
                f"Provider mismatch, expected {self.name}, got {tokens[0]}"
            )
        return Resource(
            id=tokens[3],
            provider=tokens[1],
            type=tokens[2],
        )
