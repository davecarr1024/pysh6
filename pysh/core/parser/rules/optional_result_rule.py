from abc import abstractmethod
from dataclasses import dataclass
from pysh.core.parser import results, states
from pysh.core.parser.rules import rule, rule_error, scope


@dataclass(frozen=True)
class OptionalResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: states.State, scope: scope.Scope[results.Result]
    ) -> states.StateAndOptionalResult[results.Result]:
        ...

    def optional(self) -> "OptionalResultRule[results.Result]":
        return self

    def single(self) -> "single_result_rule.SingleResultRule[results.Result]":
        raise rule_error.RuleError(
            rule=self, msg="unable to convert OptionalResultRule to SingleResultRule"
        )


from pysh.core.parser.rules import single_result_rule