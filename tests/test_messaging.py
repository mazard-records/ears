import json
from base64 import b64encode
from os import environ
from unittest.mock import Mock

from pydantic import BaseModel

from ears.messaging import EventPublisher, PublisherSettings, pydantic_model_from_event


def test_publisher_settings() -> None:
    environ.update(GOOGLE_PROJECT_ID="ears")
    settings = PublisherSettings()
    assert settings.project == "ears"


def test_event_publisher(publisher_mock: Mock) -> None:
    publisher = EventPublisher("cipot")
    message = {"foo": "bar"}
    publisher(message)
    publisher_mock.assert_called_once_with(
        "projects/ears/topics/cipot",
        json.dumps(message).encode("utf-8"),
    )


class _Model(BaseModel):
    foo: str


def test_pydantic_model_from_event() -> None:
    event = {"data": b64encode('{"foo": "bar"}'.encode("utf-8"))}
    model = pydantic_model_from_event(_Model, event)
    assert model.foo == "bar"
