from dataclasses import dataclass
from typing import TypeVar
from pysh.core import lexer
from pysh.core.parser import results, states
from pysh.core.parser.rules import single_results_rule


_State = TypeVar("_State")
_Result = TypeVar("_Result", covariant=True)


@dataclass(frozen=True)
class Constant(single_results_rule.SingleResultsRule[_State, _Result]):
    value: _Result

    def __call__(self, state: _State) -> states.StateAndSingleResults[_State, _Result]:
        return states.StateAndSingleResults[_State, _Result](
            state,
            results.SingleResults[_Result](self.value),
        )
