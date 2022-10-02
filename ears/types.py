from typing import Any, Callable, Dict, TypeVar, Union

from pydantic import BaseModel

Event = Dict[str, Any]
PydanticModel = TypeVar("PydanticModel", bound=BaseModel)
PydanticEvent = Union[Event, BaseModel]
EventPublisherType = Callable[[Union[Dict[str, Any], PydanticEvent]], None]
