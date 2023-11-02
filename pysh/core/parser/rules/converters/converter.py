from dataclasses import dataclass, field
from typing import Generic, Optional
from pysh.core.parser import results
from pysh.core.parser.rules import child_rule, scope as scope_lib, single_result_rule
from pysh.core.parser.rules.unary_rules import unary_rule


@dataclass(frozen=True)
class Converter(
    Generic[results.Result, results.ConverterResult, child_rule.ChildRule],
    single_result_rule.SingleResultRule[results.ConverterResult],
    unary_rule.UnaryRule[results.ConverterResult, child_rule.ChildRule],
):
    scope: Optional[scope_lib.Scope[results.Result]] = field(default=None, kw_only=True)

    def __str__(self) -> str:
        return str(self.child)

    def _scope(self) -> scope_lib.Scope[results.Result]:
        return self.scope or scope_lib.Scope[results.Result]()
