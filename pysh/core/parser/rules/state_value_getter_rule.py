from dataclasses import dataclass, field
from typing import Generic, TypeVar
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result", covariant=True)
_Value = TypeVar("_Value", covariant=True)


@dataclass(frozen=True)
class StateValueGetterRule(
    Generic[_State, _Result, _Value],
    rule.Rule[_State, _Result],
):
    state_value_getter: states.StateValueGetter[_State, _Value] = field(
        hash=False,
        repr=False,
        compare=False,
    )

    def _get_state_value(self, state: _State) -> _Value:
        return self.state_value_getter.get(state)
