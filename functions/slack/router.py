from typing import Any, Callable, Dict, Optional
from urllib.parse import urlparse

from flask import Response

HTTPHandler = Callable[[str], Optional[Response]]


class Router(object):

    SCHEME = "ears"

    def __init__(self) -> None:
        self._handlers: Dict[str, HTTPHandler] = {}

    def register(
        self,
        domain: str,
        handler: HTTPHandler,
    ) -> None:
        self._handlers[domain] = handler

    def serve(self, url: str) -> Optional[Response]:
        resource = urlparse(url)
        if resource.scheme != self.SCHEME:
            raise ValueError(f"Invalid url scheme {resource.scheme}")
        if resource.netloc not in self._handlers:
            raise ValueError(f"Invalid domain {resource.netloc}")
        return self._handlers[resource.netloc](resource.path)
