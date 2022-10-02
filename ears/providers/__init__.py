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
        resource = Resource.from_urn(urn)
        if resource.provider != self.name:
            raise ValueError(
                f"Provider mismatch, expected {self.name}," f" got {resource.provider}"
            )
        return resource
