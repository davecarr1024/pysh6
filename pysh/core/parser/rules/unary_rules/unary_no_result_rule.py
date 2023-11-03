from dataclasses import dataclass
from pysh.core.parser import results, states
from pysh.core.parser.rules import child_rule, no_result_rule, scope
from pysh.core.parser.rules.unary_rules import unary_rule


@dataclass(frozen=True)
class UnaryNoResultRule(
    unary_rule.UnaryRule[results.Result, child_rule.ChildRule],
    no_result_rule.NoResultRule[results.Result],
):
    def __call__(
        self, state: "states.State", scope: "scope.Scope[results.Result]"
    ) -> "states.StateAndNoResult[results.Result]":
        return self._call(state, scope).no()
