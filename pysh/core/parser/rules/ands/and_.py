from dataclasses import dataclass
from typing import TypeVar
from pysh.core.parser.rules import nary_rule, rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_ChildRuleType = TypeVar("_ChildRuleType", bound=rule.Rule, covariant=True)


@dataclass(frozen=True)
class And(
    nary_rule.NaryRule[
        _State,
        _Result,
        _ChildRuleType,
    ]
):
    def __str__(self) -> str:
        return f"({' & '.join(map(str,self))})"
