import json
from base64 import b64decode
from functools import lru_cache
from typing import Any, Dict, Type

from google.cloud.pubsub_v1 import PublisherClient as _PublisherClient  # type: ignore
from pydantic import BaseSettings, Field

from .types import Producer, PydanticModel


class _PublisherSettings(BaseSettings):
    project: str = Field(..., env="GOOGLE_PROJECT_ID")


@lru_cache(maxsize=1)
def PublisherSettings() -> _PublisherSettings:
    return _PublisherSettings()


@lru_cache(maxsize=1)
def PublisherClient() -> _PublisherClient:
    return _PublisherClient()


@lru_cache(maxsize=10)
def EventPublisher(topic: str) -> Producer:
    client = PublisherClient()
    settings = PublisherSettings()
    topic = f"projects/{settings.project}/topics/{topic}"

    def publish(message: Dict[str, Any]) -> None:
        future = client.publish(
            topic,
            json.dumps(message).encode("utf-8"),
        )
        future.result()

    return publish


def pydantic_model_from_event(
    model: Type[PydanticModel],
    event: Dict[str, Any],
) -> PydanticModel:
    if "data" not in event:
        raise ValueError("Missing event data")
    payload = b64decode(event["data"]).decode("utf-8")
    return model(**json.loads(payload))
