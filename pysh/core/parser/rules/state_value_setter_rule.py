from dataclasses import dataclass, field
from typing import Generic, TypeVar
from pysh.core.parser import states
from pysh.core.parser.rules import rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_Value = TypeVar("_Value")


@dataclass(frozen=True)
class StateValueSetterRule(
    Generic[_State, _Result, _Value],
    rule.Rule[_State, _Result],
):
    state_value_setter: states.StateValueSetter[_State, _Value] = field(
        hash=False,
        repr=False,
        compare=False,
    )

    def _get_state_value(self, state: _State) -> _Value:
        return self.state_value_setter.get(state)

    def _set_state_value(self, state: _State, value: _Value) -> _State:
        return self.state_value_setter.set(state, value)
