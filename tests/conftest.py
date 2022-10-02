from os import environ
from typing import cast
from unittest.mock import Mock

from pytest import fixture
from pytest_mock import MockerFixture


@fixture(scope="function")
def publisher_mock(mocker: MockerFixture) -> Mock:
    environ.update(GOOGLE_PROJECT_ID="ears")
    future = mocker.MagicMock()
    future.result = mocker.Mock()
    client = mocker.MagicMock()
    client.publish = mocker.Mock(return_value=future)
    mocker.patch("ears.messaging.PublisherClient", return_value=client)
    return cast(Mock, client.publish)
