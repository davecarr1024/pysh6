from dataclasses import dataclass
from .. import chars, errors
from . import unary_regex, state_and_result, result, error


@dataclass(frozen=True)
class OneOrMore(unary_regex.UnaryRegex):
    def __str__(self) -> str:
        return f"{self.child}+"

    def __call__(self, state: chars.Stream) -> state_and_result.StateAndResult:
        try:
            state, result = self.child(state)
        except errors.Error as error_:
            raise error.Error(regex=self, state=state, children=[error_])
        while True:
            try:
                state, child_result = self.child(state)
                result += child_result
            except errors.Error:
                return state, result
