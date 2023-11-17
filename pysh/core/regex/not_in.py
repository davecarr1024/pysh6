from dataclasses import dataclass
from typing import Sequence
from pysh.core.regex import error, state, state_and_result, unary_regex


@dataclass(frozen=True)
class NotIn(unary_regex.UnaryRegex):
    values: Sequence[str]

    def __str__(self) -> str:
        return f"({self.child} not in {self.values})"

    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        child_state_and_result = self._call_child(state)
        if child_state_and_result.result.value() in self.values:
            raise self._error(
                state, msg=f"invalid value {child_state_and_result.result.value()}"
            )
        return child_state_and_result
