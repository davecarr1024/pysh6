from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, overload
from pysh.core import lexer
from pysh.core.parser import errors, results
from pysh.core.parser.rules import rule


@dataclass(frozen=True)
class SingleResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: "states.State", scope: "scope.Scope[results.Result]"
    ) -> "states.StateAndSingleResult[results.Result]":
        ...

    def single(self) -> "SingleResultRule[results.Result]":
        return self

    @overload
    def __and__(
        self, rhs: "no_result_rule.NoResultRule[results.Result]"
    ) -> "single_result_and.SingleResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "SingleResultRule[results.Result]"
    ) -> "multiple_result_and.MultipleResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "optional_result_rule.OptionalResultRule[results.Result]"
    ) -> "multiple_result_and.MultipleResultAnd[results.Result]":
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
    def __and__(self, rhs: str) -> "single_result_and.SingleResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "lexer.Rule"
    ) -> "single_result_and.SingleResultAnd[results.Result]":
        ...

    def __and__(
        self, rhs: "and_args.AndArgs"
    ) -> "and_.And[results.Result, rule.Rule[results.Result]]":
        if isinstance(rhs, no_result_rule.NoResultRule):
            return single_result_and.SingleResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, SingleResultRule):
            return multiple_result_and.MultipleResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, optional_result_rule.OptionalResultRule):
            return multiple_result_and.MultipleResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, multiple_result_rule.MultipleResultRule):
            return multiple_result_and.MultipleResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, named_result_rule.NamedResultRule):
            return named_result_and.NamedResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, str) or isinstance(rhs, lexer.Rule):
            return single_result_and.SingleResultAnd[results.Result](
                [
                    self,
                    no_result_literal.NoResultLiteral[results.Result].load(rhs),
                ]
            )
        else:
            raise errors.RuleError(rule=self, msg=f"unknown and rhs type {type(rhs)}")

    @overload
    def __rand__(self, lhs: str) -> "single_result_and.SingleResultAnd[results.Result]":
        ...

    @overload
    def __rand__(
        self, lhs: "lexer.Rule"
    ) -> "single_result_and.SingleResultAnd[results.Result]":
        ...

    def __rand__(
        self, lhs: "rand_args.RandArgs"
    ) -> "single_result_and.SingleResultAnd[results.Result]":
        return no_result_literal.NoResultLiteral[results.Result].load(lhs) & self

    @overload
    def __or__(
        self, rhs: "no_result_rule.NoResultRule[results.Result]"
    ) -> "optional_result_or.OptionalResultOr[results.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "SingleResultRule[results.Result]"
    ) -> "single_result_or.SingleResultOr[results.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_result_rule.OptionalResultRule[results.Result]"
    ) -> "optional_result_or.OptionalResultOr[results.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "multiple_result_rule.MultipleResultRule[results.Result]"
    ) -> "multiple_result_or.MultipleResultOr[results.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "named_result_rule.NamedResultRule[results.Result]"
    ) -> "named_result_or.NamedResultOr[results.Result]":
        ...

    def __or__(
        self, rhs: "or_args.OrArgs[results.Result]"
    ) -> "or_.Or[results.Result,rule.Rule[results.Result]]":
        if isinstance(rhs, no_result_rule.NoResultRule):
            return optional_result_or.OptionalResultOr[results.Result]([self, rhs])
        elif isinstance(rhs, SingleResultRule):
            return single_result_or.SingleResultOr[results.Result]([self, rhs])
        elif isinstance(rhs, optional_result_rule.OptionalResultRule):
            return optional_result_or.OptionalResultOr[results.Result]([self, rhs])
        elif isinstance(rhs, multiple_result_rule.MultipleResultRule):
            return multiple_result_or.MultipleResultOr[results.Result]([self, rhs])
        elif isinstance(rhs, named_result_rule.NamedResultRule):
            return named_result_or.NamedResultOr[results.Result]([self, rhs])
        else:
            raise errors.RuleError(rule=self, msg=f"unknown or rhs type {type(rhs)}")

    def convert(
        self,
        func: "results.SingleResultConverterFunc[results.Result, results.ConverterResult]",
        scope: Optional["scope.Scope[results.Result]"] = None,
    ) -> "single_result_converter.SingleResultConverter[results.Result,results.ConverterResult]":
        return single_result_converter.SingleResultConverter[
            results.Result, results.ConverterResult
        ](self, func, scope=scope)


from pysh.core.parser import states
from pysh.core.parser.rules import (
    scope,
    no_result_rule,
    optional_result_rule,
    multiple_result_rule,
    named_result_rule,
)
from pysh.core.parser.rules.ands import (
    and_,
    and_args,
    rand_args,
    single_result_and,
    multiple_result_and,
    named_result_and,
)
from pysh.core.parser.rules.literals import no_result_literal
from pysh.core.parser.rules.converters import single_result_converter
from pysh.core.parser.rules.ors import (
    or_,
    or_args,
    single_result_or,
    optional_result_or,
    multiple_result_or,
    named_result_or,
)
