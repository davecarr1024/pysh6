from dataclasses import dataclass
from pysh.core.regex import result, state


@dataclass(frozen=True)
class StateAndResult:
    state: state.State
    result: result.Result
