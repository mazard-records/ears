from typing import Any, Callable, Dict, TypeVar

from pydantic import BaseModel

DomainHandler = Callable[[str], None]
Producer = Callable[[Dict[str, Any]], None]
PydanticModel = TypeVar("PydanticModel", bound=BaseModel)
