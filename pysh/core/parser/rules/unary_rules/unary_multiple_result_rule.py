from dataclasses import dataclass
from pysh.core.parser import results, states
from pysh.core.parser.rules import child_rule, multiple_result_rule, scope
from pysh.core.parser.rules.unary_rules import unary_rule_with_scope


@dataclass(frozen=True)
class UnaryMultipleResultRule(
    unary_rule_with_scope.UnaryRuleWithScope[results.Result, child_rule.ChildRule],
    multiple_result_rule.MultipleResultRule[results.Result],
):
    def __call__(
        self, state: "states.State", scope: "scope.Scope[results.Result]"
    ) -> "states.StateAndMultipleResult[results.Result]":
        return super().__call__(state, scope | self.scope).multiple()
