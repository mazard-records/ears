from typing import Any, Callable, Dict, TypeVar

from pydantic import BaseModel

Event = Dict[str, Any]
Producer = Callable[[Dict[str, Any]], None]
PydanticModel = TypeVar("PydanticModel", bound=BaseModel)
