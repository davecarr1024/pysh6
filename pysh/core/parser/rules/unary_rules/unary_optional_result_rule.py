from dataclasses import dataclass
from pysh.core.parser import results, states
from pysh.core.parser.rules import child_rule, optional_result_rule, scope
from pysh.core.parser.rules.unary_rules import unary_rule_with_scope


@dataclass(frozen=True)
class UnaryOptionalResultRule(
    unary_rule_with_scope.UnaryRuleWithScope[results.Result, child_rule.ChildRule],
    optional_result_rule.OptionalResultRule[results.Result],
):
    def __call__(
        self, state: "states.State", scope: "scope.Scope[results.Result]"
    ) -> "states.StateAndOptionalResult[results.Result]":
        return super().__call__(state, scope | self.scope).optional()
