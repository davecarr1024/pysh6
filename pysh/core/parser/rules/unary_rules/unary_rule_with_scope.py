from dataclasses import dataclass, field
from pysh.core.parser import results, states
from pysh.core.parser.rules import child_rule, scope as scope_lib
from pysh.core.parser.rules.unary_rules import unary_rule


@dataclass(frozen=True)
class UnaryRuleWithScope(unary_rule.UnaryRule[results.Result, child_rule.ChildRule]):
    scope: scope_lib.Scope[results.Result] = field(
        default_factory=scope_lib.Scope[results.Result], kw_only=True
    )

    def __call__(
        self, state: states.State, scope: scope_lib.Scope[results.Result]
    ) -> states.StateAndResult[results.Result]:
        return self.child(state, scope | self.scope)
