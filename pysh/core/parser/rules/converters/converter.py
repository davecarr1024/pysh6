from dataclasses import dataclass
from typing import Generic
from pysh.core.parser import results
from pysh.core.parser.rules import child_rule, single_result_rule
from pysh.core.parser.rules.unary_rules import unary_rule_with_scope


@dataclass(frozen=True)
class Converter(
    Generic[results.Result, child_rule.ChildRule],
    single_result_rule.SingleResultRule[results.Result],
    unary_rule_with_scope.UnaryRuleWithScope[results.Result, child_rule.ChildRule],
):
    ...
