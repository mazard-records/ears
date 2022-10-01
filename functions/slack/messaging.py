import json

from functools import lru_cache
from typing import Any, Callable, Dict

from google.cloud.pubsub_v1 import PublisherClient as _PublisherClient
from pydantic import BaseSettings, Field


Producer = Callable[[Dict[str, Any]], None]


class _PublisherSettings(BaseSettings):
    prefix: str = Field(..., env="PUBLISHER_PREFIX")
    project: str = Field(..., env="GCP_PROJECT")


@lru_cache(maxsize=1)
def PublisherSettings() -> _PublisherSettings:
    return _PublisherSettings()


@lru_cache(maxsize=1)
def PublisherClient() -> _PublisherClient:
    return _PublisherClient()


@lru_cache(maxsize=10)
def MessageProducer(provider: str) -> Producer:
    client = PublisherClient()
    settings = PublisherSettings()
    topic = "/".join([
        "projects",
        settings.project,
        "topics",
        f"{settings.prefix}{provider}"
    ])

    def publish(message: Dict[str, Any]) -> None:
        future = client.publish(topic, json.dumps(message).encode("utf-8"))
        future.result()

    return publish