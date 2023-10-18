from dataclasses import dataclass
from typing import Generic
from pysh.core.processor import results, states
from pysh.core.processor.errors import error


@dataclass(kw_only=True)
class RuleError(error.Error, Generic[states.State, results.Result]):
    rule: "rule.Rule[states.State,results.Result]"


from pysh.core.processor.rules import rule
