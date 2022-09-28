import hmac

from functools import lru_cache
from hashlib import sha256
from typing import Callable

from flask import Request, Response
from pydantic import AnyHttpUrl, BaseSettings, Field

FlaskEndpoint = Callable[[Request], Response]


class _Settings(BaseSettings):
    signing: str = Field(..., env="SIGNING_KEY")
    version: str = Field("v0", env="VERSION")
    webhook: AnyHttpUrl = Field(..., env="WEBHOOK")

    class Config:
        env_prefix = "SLACK"


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
            message = f"{settings.version}:{timestamp}:{body}"
            signature = hmac.new(
                bytes(settings.signing),
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
    