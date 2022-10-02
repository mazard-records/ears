from abc import ABC, abstractproperty, abstractmethod
from typing import List

from ..models import PlaylistEvent, Resource, Track, TrackSearchQuery


class AbstractMusicProvider(ABC):
    """
    A music provi
    """
    
    @abstractproperty
    def name(self) -> str:
        pass

    @abstractmethod
    def get_playlist(self, event: PlaylistEvent) -> List[Track]:
        pass

    @abstractmethod
    def add_to_playlist(self, event: PlaylistEvent) -> None:
        pass

    @abstractmethod
    def remove_from_playlist(self, event: PlaylistEvent) -> None:
        pass

    @abstractmethod
    def search(
        self,
        query: TrackSearchQuery,
    ) -> List[Track]:
        pass

    def parse_urn(self, urn: str) -> Resource:
        """
        Parse the given URN into a target TrackSource.
        Such URN are designed as follow:

        urn:PROVIDER:IDENTIFIER

        Where given provider should match this object target.
        """
        tokens = urn.split(":")
        if len(tokens) != 3 or tokens[0] != "urn":
            raise ValueError(f"Invalid urn {urn}")
        if tokens[1] != self.name:
            raise ValueError(
                f"Provider mismatch, expected {self.name}, got {tokens[0]}"
            )
        return Resource(identifier=tokens[2], provider=tokens[1])