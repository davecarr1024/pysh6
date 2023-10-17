from dataclasses import dataclass
from typing import Generic
from pysh.core.parser.errors import error
from pysh.core.parser.state_and_result import result


@dataclass(kw_only=True)
class RuleError(error.Error, Generic[result.Result]):
    rule: "rule.Rule[result.Result]"


from pysh.core.parser.rules import rule
