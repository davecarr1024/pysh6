from dataclasses import dataclass
from typing import Union
from pysh.core import errors
from pysh.core.regex import (
    literal,
    or_,
    range,
    result,
    state,
    state_and_result,
    unary_regex,
)


@dataclass(frozen=True)
class Not(
    unary_regex.UnaryRegex[
        Union[
            literal.Literal,
            range.Range,
            or_.Or[
                Union[
                    literal.Literal,
                    range.Range,
                ]
            ],
        ]
    ]
):
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
        raise self._error(state=state, msg=f"child of not {self.child} applied")
