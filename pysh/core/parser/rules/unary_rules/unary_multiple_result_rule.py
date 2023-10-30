from dataclasses import dataclass
from pysh.core.parser import results, states

from pysh.core.parser.rules import child_rule, multiple_result_rule, scope
from pysh.core.parser.rules.unary_rules import unary_rule


@dataclass(frozen=True)
class UnaryMultipleResultRule(
    multiple_result_rule.MultipleResultRule[results.Result],
    unary_rule.UnaryRule[results.Result, child_rule.ChildRule],
):
    def __call__(
        self, state: states.State, scope: scope.Scope
    ) -> states.StateAndMultipleResult[results.Result]:
        return self.child(state, scope).multiple()
