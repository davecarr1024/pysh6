from dataclasses import dataclass
from typing import Generic, TypeVar
from pysh.core.parser.errors import error

_Result = TypeVar("_Result")


@dataclass(kw_only=True)
class RuleError(error.Error, Generic[_Result]):
    rule: "rule.Rule[_Result]"


from pysh.core.parser.rules import rule
