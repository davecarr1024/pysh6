from abc import abstractmethod
from dataclasses import dataclass
from typing import overload
from pysh.core import lexer
from pysh.core.parser import errors, results
from pysh.core.parser.rules import rule


@dataclass(frozen=True)
class MultipleResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: "states.State[results.Result]"
    ) -> "states.StateAndMultipleResult[results.Result]":
        ...

    def multiple(self) -> "MultipleResultRule[results.Result]":
        return self

    @overload
    def __and__(
        self, rhs: "no_result_rule.NoResultRule[results.Result]"
    ) -> "multiple_result_and.MultipleResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "single_result_rule.SingleResultRule[results.Result]"
    ) -> "multiple_result_and.MultipleResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "optional_result_rule.OptionalResultRule[results.Result]"
    ) -> "multiple_result_and.MultipleResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "MultipleResultRule[results.Result]"
    ) -> "multiple_result_and.MultipleResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "named_result_rule.NamedResultRule[results.Result]"
    ) -> "named_result_and.NamedResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: str
    ) -> "multiple_result_and.MultipleResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "lexer.Rule"
    ) -> "multiple_result_and.MultipleResultAnd[results.Result]":
        ...

    def __and__(
        self, rhs: "and_args.AndArgs"
    ) -> "and_.And[results.Result, rule.Rule[results.Result]]":
        if isinstance(rhs, no_result_rule.NoResultRule):
            return multiple_result_and.MultipleResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, single_result_rule.SingleResultRule):
            return multiple_result_and.MultipleResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, optional_result_rule.OptionalResultRule):
            return multiple_result_and.MultipleResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, MultipleResultRule):
            return multiple_result_and.MultipleResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, named_result_rule.NamedResultRule):
            return named_result_and.NamedResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, str) or isinstance(rhs, lexer.Rule):
            return multiple_result_and.MultipleResultAnd[results.Result](
                [
                    self,
                    no_result_literal.NoResultLiteral[results.Result].load(rhs),
                ]
            )
        else:
            raise errors.RuleError(rule=self, msg=f"unknown and rhs type {type(rhs)}")


from pysh.core.parser import states
from pysh.core.parser.rules import (
    no_result_rule,
    single_result_rule,
    optional_result_rule,
    named_result_rule,
)
from pysh.core.parser.rules.ands import (
    and_,
    and_args,
    multiple_result_and,
    named_result_and,
)
from pysh.core.parser.rules.literals import no_result_literal
