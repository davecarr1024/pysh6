from dataclasses import dataclass
from typing import Generic
from pysh.core.parser import results, states
from pysh.core.parser.errors import error


@dataclass(kw_only=True)
class RuleError(error.Error, Generic[results.Result]):
    rule: "rule.Rule[results.Result]"


from pysh.core.parser.rules import rule
