from dataclasses import dataclass

from pysh.core.parser.errors import error
from pysh.core.parser.state import state


@dataclass(kw_only=True)
class StateError(error.Error):
    state: state.State
