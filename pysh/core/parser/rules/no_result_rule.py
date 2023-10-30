from abc import abstractmethod
from dataclasses import dataclass
from pysh.core.parser import results, states
from pysh.core.parser.rules import rule_error, rule, scope


@dataclass(frozen=True)
class NoResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: states.State, scope: scope.Scope[results.Result]
    ) -> states.StateAndNoResult[results.Result]:
        ...

    def no(self) -> "NoResultRule[results.Result]":
        return self

    def single(self) -> "single_result_rule.SingleResultRule[results.Result]":
        raise rule_error.RuleError(
            rule=self, msg="unable to convert NoResultRule to SingleResultRule"
        )


from pysh.core.parser.rules import single_result_rule
