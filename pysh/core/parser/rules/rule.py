from abc import ABC
from typing import Generic, TypeVar


_Result = TypeVar("_Result")


class Rule(ABC, Generic[_Result]):
    ...
