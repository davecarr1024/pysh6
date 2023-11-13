from dataclasses import dataclass
from typing import TypeVar
from pysh.core.parser import states
from pysh.core.parser.rules import nary_rule, rule


_State = TypeVar("_State", bound=states.State)
_Result = TypeVar("_Result", covariant=True)
_ChildRuleType = TypeVar("_ChildRuleType", bound=rule.Rule, covariant=True)


@dataclass(frozen=True)
class Or(
    nary_rule.NaryRule[
        _State,
        _Result,
        _ChildRuleType,
    ]
):
    def __str__(self) -> str:
        return f"({' | '.join(map(str,self))})"
