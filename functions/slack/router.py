from typing import Any, Callable, Optional
from urllib.parse import urlparse

from flask import Response

HTTPHandler = Callable[[str], Optional[Response]]


class Router(object):

    SCHEME = "ears"

    def __init__(self) -> None:
        self._handlers = {}

    def registry_handler(
        self,
        domain: str,
        handler: HTTPHandler,
    ) -> None:
        self._handlers[domain] = handler

    def serve(self, url: str) -> Optional[Response]:
        resource = urlparse(url)
        if resource.scheme != self.SCHEME:
            raise ValueError(f"Invalid url scheme {url.scheme}")
        if resource.netloc not in self._http_request_handlers:
            raise ValueError(f"Invalid domain {resource.netloc}")
        return self._handlers[resource.netloc](resource.path)
