from httpx import Client

from ._mixins import (
    AuthorizationTransportMixin,
    SearchTransportMixin,
    PlaylistTransportMixin,
)


class BeatportTransport(
    AuthorizationTransportMixin,
    SearchTransportMixin,
    PlaylistTransportMixin,
):

    URL = "https://www.beatport.com"
    USER_AGENT =  (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/15.1 Safari/605.1.15"
    )

    def __init__(self) -> None:
        self._transport = Client(
            base_url=self.URL,
            headers={
                "User-Agent": self.USER_AGENT,
                "Origin": self.URL,
                "Referer": f"{self.URL}/",
            },
        )

    @property
    def transport(self) -> Client:
        return self._transport
