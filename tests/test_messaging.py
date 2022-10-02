from base64 import b64encode
from os import environ

from pydantic import BaseModel

from ears.messaging import (
    PublisherSettings,
    PublisherClient,
    MessageProducer,
    pydantic_model_from_event,
)


def test_publisher_settings() -> None:
    environ.update(EARS_PUBLISHER_PREFIX="tympan")
    environ.update(GOOGLE_PROJECT_ID="ears")
    settings = PublisherSettings()
    assert id(settings) == id(PublisherSettings())
    assert settings.prefix == "tympan"
    assert settings.project == "ears"


def test_publisher_client() -> None:
    assert id(PublisherClient()) == id(PublisherClient())


def test_message_producer() -> None:
    pass


class _Model(BaseModel):
    foo: str


def test_pydantic_model_from_event() -> None:
    event = {"data": b64encode('{"foo": "bar"}'.encode("utf-8"))}
    model = pydantic_model_from_event(_Model, event)
    assert model.foo == "bar"
