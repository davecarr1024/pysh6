from dataclasses import dataclass
from typing import Optional
from pysh.core.parser import results, states

from pysh.core.parser.rules import child_rule, named_result_rule, scope
from pysh.core.parser.rules.unary_rules import unary_rule


@dataclass(frozen=True)
class UnaryNamedResultRule(
    named_result_rule.NamedResultRule[results.Result],
    unary_rule.UnaryRule[results.Result, child_rule.ChildRule],
):
    name: Optional[str] = None

    def __call__(
        self, state: states.State, scope: scope.Scope
    ) -> states.StateAndNamedResult[results.Result]:
        return self.child(state, scope).named(self.name)
