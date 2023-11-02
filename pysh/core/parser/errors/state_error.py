from dataclasses import dataclass
from pysh.core.parser import states
from pysh.core.parser.errors import error


@dataclass(kw_only=True, repr=False)
class StateError(error.Error):
    state: states.State

    def _repr_line(self) -> str:
        return f"StateError({self.state},msg={self.msg})"
