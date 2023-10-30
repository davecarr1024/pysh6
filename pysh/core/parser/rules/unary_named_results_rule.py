from dataclasses import dataclass
from pysh.core.parser import results, states

from pysh.core.parser.rules import child_rule, named_results_rule, scope, unary_rule


@dataclass(frozen=True)
class UnaryNamedResultsRule(
    named_results_rule.NamedResultsRule[results.Result],
    unary_rule.UnaryRule[results.Result, child_rule.ChildRule],
):
    name: str

    def __call__(
        self, state: states.State, scope: scope.Scope
    ) -> states.StateAndNamedResults[results.Result]:
        return self.child(state, scope).named(self.name)
