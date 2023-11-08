from dataclasses import dataclass
from pysh.core.lexer import result, state


@dataclass(frozen=True)
class StateAndResult:
    state: state.State
    result: result.Result
