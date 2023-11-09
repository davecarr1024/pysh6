from dataclasses import dataclass
from typing import Generic, TypeVar
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_Value = TypeVar("_Value")


@dataclass(frozen=True)
class StateValueGetterRule(
    Generic[_State, _Result, _Value],
    rule.Rule[_State, _Result],
):
    state_value_getter: states.StateValueGetter[_State, _Value]

    def _get_state_value(self, state: _State) -> _Value:
        return self.state_value_getter.get(state)
