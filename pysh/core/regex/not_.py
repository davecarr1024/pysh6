from dataclasses import dataclass
from pysh.core import errors
from pysh.core.regex import result, state, state_and_result, unary_regex


@dataclass(frozen=True)
class Not(unary_regex.UnaryRegex):
    def __str__(self) -> str:
        return f"^{self.child}"

    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        try:
            super().__call__(state)
        except errors.Error:
            return state_and_result.StateAndResult(state.tail(), result.Result())
        raise self._error(state, msg=f"child of not {self.child} applied")
