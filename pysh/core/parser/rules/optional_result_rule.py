from abc import abstractmethod
from dataclasses import dataclass
from pysh.core.parser import errors, results
from pysh.core.parser.rules import rule


@dataclass(frozen=True)
class OptionalResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: "states.State"
    ) -> "states.StateAndOptionalResult[results.Result]":
        ...

    def optional(self) -> "OptionalResultRule[results.Result]":
        return self

    def single(self) -> "single_result_rule.SingleResultRule[results.Result]":
        raise errors.RuleError(
            rule=self, msg="unable to convert OptionalResultRule to SingleResultRule"
        )


from pysh.core.parser import states
from pysh.core.parser.rules import single_result_rule
