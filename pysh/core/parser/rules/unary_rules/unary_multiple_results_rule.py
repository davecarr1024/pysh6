from dataclasses import dataclass
from pysh.core.parser import results, states

from pysh.core.parser.rules import child_rule, multiple_results_rule, scope
from pysh.core.parser.rules.unary_rules import unary_rule


@dataclass(frozen=True)
class UnaryMultipleResultsRule(
    multiple_results_rule.MultipleResultsRule[results.Result],
    unary_rule.UnaryRule[results.Result, child_rule.ChildRule],
):
    def __call__(
        self, state: states.State, scope: scope.Scope
    ) -> states.StateAndMultipleResults[results.Result]:
        return self.child(state, scope).multiple()
