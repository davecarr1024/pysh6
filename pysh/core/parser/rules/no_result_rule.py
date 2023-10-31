from abc import abstractmethod
from dataclasses import dataclass
from typing import overload
from pysh.core import lexer
from pysh.core.parser import errors, results
from pysh.core.parser.rules import rule


@dataclass(frozen=True)
class NoResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: "states.State[results.Result]"
    ) -> "states.StateAndNoResult[results.Result]":
        ...

    def no(self) -> "NoResultRule[results.Result]":
        return self

    def single(self) -> "single_result_rule.SingleResultRule[results.Result]":
        raise errors.RuleError(
            rule=self, msg="unable to convert NoResultRule to SingleResultRule"
        )

    @overload
    def __and__(
        self, rhs: "NoResultRule[results.Result]"
    ) -> "no_result_and.NoResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "single_result_rule.SingleResultRule[results.Result]"
    ) -> "single_result_and.SingleResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "optional_result_rule.OptionalResultRule[results.Result]"
    ) -> "optional_result_and.OptionalResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "multiple_result_rule.MultipleResultRule[results.Result]"
    ) -> "multiple_result_and.MultipleResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "named_result_rule.NamedResultRule[results.Result]"
    ) -> "named_result_and.NamedResultAnd[results.Result]":
        ...

    @overload
    def __and__(self, rhs: str) -> "no_result_and.NoResultAnd[results.Result]":
        ...

    @overload
    def __and__(self, rhs: "lexer.Rule") -> "no_result_and.NoResultAnd[results.Result]":
        ...

    def __and__(
        self, rhs: "and_args.AndArgs"
    ) -> "and_.And[results.Result, rule.Rule[results.Result]]":
        if isinstance(rhs, NoResultRule):
            return no_result_and.NoResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, single_result_rule.SingleResultRule):
            return single_result_and.SingleResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, optional_result_rule.OptionalResultRule):
            return optional_result_and.OptionalResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, multiple_result_rule.MultipleResultRule):
            return multiple_result_and.MultipleResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, named_result_rule.NamedResultRule):
            return named_result_and.NamedResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, str) or isinstance(rhs, lexer.Rule):
            return no_result_and.NoResultAnd[results.Result](
                [
                    self,
                    no_result_literal.NoResultLiteral[results.Result].load(rhs),
                ]
            )
        else:
            raise errors.RuleError(rule=self, msg=f"unknown and rhs type {type(rhs)}")

    @overload
    def __rand__(self, lhs: str) -> "no_result_and.NoResultAnd[results.Result]":
        ...

    @overload
    def __rand__(
        self, lhs: "lexer.Rule"
    ) -> "no_result_and.NoResultAnd[results.Result]":
        ...

    def __rand__(
        self, lhs: "rand_args.RandArgs"
    ) -> "no_result_and.NoResultAnd[results.Result]":
        return no_result_literal.NoResultLiteral[results.Result].load(lhs) & self


from pysh.core.parser import states
from pysh.core.parser.rules import (
    single_result_rule,
    optional_result_rule,
    multiple_result_rule,
    named_result_rule,
)
from pysh.core.parser.rules.ands import (
    and_,
    and_args,
    no_result_and,
    rand_args,
    single_result_and,
    optional_result_and,
    multiple_result_and,
    named_result_and,
)
from pysh.core.parser.rules.literals import no_result_literal
