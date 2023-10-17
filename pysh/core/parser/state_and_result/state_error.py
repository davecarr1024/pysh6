from dataclasses import dataclass

from pysh.core.parser import errors
from pysh.core.parser.state_and_result import state


@dataclass(kw_only=True)
class StateError(errors.Error):
    state_: state.State