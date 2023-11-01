from dataclasses import dataclass
from typing import Generic
from pysh.core.parser import results
from pysh.core.parser.errors import error


@dataclass(kw_only=True)
class StateError(error.Error, Generic[results.Result]):
    state: "states.State"


from pysh.core.parser import states
