from dataclasses import dataclass
from pysh.core.parser import states
from pysh.core.parser.errors import error


@dataclass(kw_only=True)
class StateError(error.Error):
    state: "states.State"
