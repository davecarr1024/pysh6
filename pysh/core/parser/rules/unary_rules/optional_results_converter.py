from dataclasses import dataclass, field
from typing import Callable, Generic, Optional, TypeVar
from pysh.core.parser import states
from pysh.core.parser.rules import single_results_rule
from pysh.core.parser.rules.unary_rules import unary_rule


_State = TypeVar("_State", bound=states.State)
_Result = TypeVar("_Result", covariant=True)
_ChildResult = TypeVar("_ChildResult")


@dataclass(frozen=True)
class OptionalResultsConverter(
    Generic[_State, _Result, _ChildResult],
    single_results_rule.SingleResultsRule[_State, _Result],
    unary_rule.UnaryRule[_State, _Result, _ChildResult],
):
    func: Callable[[Optional[_ChildResult]], _Result] = field(
        compare=False,
        hash=False,
    )

    def __call__(self, state: _State) -> states.StateAndSingleResults[_State, _Result]:
        return self._call_child(state).optional().convert(self.func)
