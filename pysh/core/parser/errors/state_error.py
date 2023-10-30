from dataclasses import dataclass
from typing import Generic
from pysh.core.parser import results, states
from pysh.core.parser.errors import error


@dataclass(kw_only=True)
class StateError(error.Error, Generic[results.Result]):
    state: "states.State[results.Result]"
