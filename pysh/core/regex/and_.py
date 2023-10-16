from dataclasses import dataclass
from .. import chars, errors
from . import nary_regex, state_and_result, error, result


@dataclass(frozen=True)
class And(nary_regex.NaryRegex):
    def __str__(self) -> str:
        return f"({''.join([str(child) for child in self])})"

    def __call__(self, state: chars.Stream) -> state_and_result.StateAndResult:
        result_ = result.Result()
        for child in self:
            try:
                state, child_result = child(state)
            except errors.Error as error_:
                raise error.Error(regex=self, state=state, children=[error_])
            result_ += child_result
        return state, result_
