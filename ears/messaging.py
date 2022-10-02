import json
from base64 import b64decode
from functools import lru_cache
from typing import Type

from google.cloud.pubsub_v1 import PublisherClient  # type: ignore
from pydantic import BaseSettings, Field

from .types import Event, EventPublisherType, PydanticEvent, PydanticModel


class PublisherSettings(BaseSettings):
    project: str = Field(..., env="GOOGLE_PROJECT_ID")


@lru_cache(maxsize=10)
def EventPublisher(topic: str) -> EventPublisherType:
    client = PublisherClient()
    settings = PublisherSettings()
    topic = f"projects/{settings.project}/topics/{topic}"

    def publish(event: PydanticEvent) -> None:
        if isinstance(event, dict):
            future = client.publish(
                topic,
                json.dumps(event).encode("utf-8"),
            )
        else:
            future = client.publish(topic, event.json().encode("utf-8"))
        future.result()

    return publish


def pydantic_model_from_event(
    model: Type[PydanticModel],
    event: Event,
) -> PydanticModel:
    if "data" not in event:
        raise ValueError("Missing event data")
    payload = b64decode(event["data"]).decode("utf-8")
    return model(**json.loads(payload))
