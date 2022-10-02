from typing import Any, Callable, Dict, Type

from pydantic import BaseModel
from slackette import Blocks

from ears.messaging import pydantic_model_from_event
from ears.types import Event, PydanticModel

ModelFactories = Dict[str, Type[BaseModel]]
BlockFactory = Callable[[BaseModel], Blocks]
BlocksFactories = Dict[str, BlockFactory]


class NotificationEvent(BaseModel):
    model: str
    data: Dict[str, Any]


class NotificationFactory(object):
    def __init__(self) -> None:
        self._model_factories: ModelFactories = {}
        self._notification_factories: BlocksFactories = {}

    def register(
        self,
        model: Type[PydanticModel],
        factory: BlockFactory,
    ) -> None:
        self._model_factories[model.__name__] = model
        self._notification_factories[model.__name__] = factory

    def create(self, event: Event) -> Blocks:
        notification_event = pydantic_model_from_event(
            NotificationEvent,
            event,
        )
        if notification_event.model not in self._model_factories:
            raise ValueError(
                f"No factory available for model {notification_event.model}"
            )
        model = self._model_factories[notification_event.model](
            **notification_event.data,
        )
        return self._notification_factories[notification_event.model](model)
