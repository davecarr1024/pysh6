from dataclasses import dataclass
from pysh.core import errors
from pysh.core.regex import literal, or_, result, state, state_and_result, unary_regex


@dataclass(frozen=True)
class Not(unary_regex.UnaryRegex[literal.Literal | or_.Or[literal.Literal]]):
    def __str__(self) -> str:
        return f"^{self.child}"

    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        try:
            self._call_child(state)
        except errors.Error:
            return state_and_result.StateAndResult(
                state.tail(),
                result.Result([state.head()]),
            )
        raise self._error(state, msg=f"child of not {self.child} applied")
