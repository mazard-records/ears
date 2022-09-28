import hmac

from functools import lru_cache
from hashlib import sha256
from typing import Callable

from flask import Request, Response
from pydantic import AnyHttpUrl, BaseSettings

FlaskEndpoint = Callable[[Request], Response]


class _Settings(BaseSettings):
    API_VERSION: str = "v0"
    SIGNING_SECRET: str
    WEBHOOK: AnyHttpUrl

    @property
    def signing_key(self) -> bytes:
        return bytes(self.SIGNING_SECRET)

    @property
    def api_version(self) -> str:
        return self.API_VERSION


@lru_cache(maxsize=1)
def SlackSettings() -> _Settings:
    """ Singleton holder through LRU cache. """
    return _Settings()


def SlackRequest(endpoint: FlaskEndpoint) -> FlaskEndpoint:
    """
    Decorator that acts as middleware to ensure that an
    incoming HTTP request is a valid issued Slack request.

    See https://api.slack.com/authentication/verifying-requests-from-slack
    """
    def middleware(request: Request) -> Response:
        try:
            expected = request.headers.get("X-Slack-Signature")
            timestamp = request.headers.get("X-Slack-Request-Timestamp")
            body = request.body()
            settings = SlackSettings()
            message = f"{settings.api_version}:{timestamp}:{body}"
            signature = hmac.new(
                settings.signing_key,
                msg=bytes(message),
                digestmod=sha256,
            )
            if signature.hexdigest() != expected:
                raise ValueError("Invalid signature")
            return endpoint(request)
        except Exception as e:
            # TODO: log
            pass
    return middleware
    