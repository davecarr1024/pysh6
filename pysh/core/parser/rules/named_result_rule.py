from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, TypeVar, overload
from pysh.core import lexer
from pysh.core.parser import errors, results
from pysh.core.parser.rules import rule

_RhsResult = TypeVar("_RhsResult")


@dataclass(frozen=True)
class NamedResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: "states.State", scope: "scope.Scope[results.Result]"
    ) -> "states.StateAndNamedResult[results.Result]":
        ...

    def named(self, name: Optional[str] = None) -> "NamedResultRule[results.Result]":
        return self

    @overload
    def __and__(
        self, rhs: "no_result_rule.NoResultRule[results.Result]"
    ) -> "named_result_and.NamedResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "single_result_rule.SingleResultRule[results.Result]"
    ) -> "named_result_and.NamedResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "optional_result_rule.OptionalResultRule[results.Result]"
    ) -> "named_result_and.NamedResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "multiple_result_rule.MultipleResultRule[results.Result]"
    ) -> "named_result_and.NamedResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "NamedResultRule[results.Result]"
    ) -> "named_result_and.NamedResultAnd[results.Result]":
        ...

    @overload
    def __and__(self, rhs: str) -> "named_result_and.NamedResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "lexer.Rule"
    ) -> "named_result_and.NamedResultAnd[results.Result]":
        ...

    def __and__(
        self, rhs: "and_args.AndArgs"
    ) -> "and_.And[results.Result, rule.Rule[results.Result]]":
        if isinstance(rhs, no_result_rule.NoResultRule):
            return named_result_and.NamedResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, single_result_rule.SingleResultRule):
            return named_result_and.NamedResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, optional_result_rule.OptionalResultRule):
            return named_result_and.NamedResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, multiple_result_rule.MultipleResultRule):
            return named_result_and.NamedResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, NamedResultRule):
            return named_result_and.NamedResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, str) or isinstance(rhs, lexer.Rule):
            return named_result_and.NamedResultAnd[results.Result](
                [
                    self,
                    no_result_literal.NoResultLiteral[results.Result].load(rhs),
                ]
            )
        else:
            raise errors.RuleError(rule=self, msg=f"unknown and rhs type {type(rhs)}")

    @overload
    def __rand__(self, lhs: str) -> "named_result_and.NamedResultAnd[results.Result]":
        ...

    @overload
    def __rand__(
        self, lhs: "lexer.Rule"
    ) -> "named_result_and.NamedResultAnd[results.Result]":
        ...

    def __rand__(
        self, lhs: "rand_args.RandArgs"
    ) -> "named_result_and.NamedResultAnd[results.Result]":
        return no_result_literal.NoResultLiteral[results.Result].load(lhs) & self

    def __matmul__(
        self, rhs: "NamedResultRule[_RhsResult]"
    ) -> "named_result_and.NamedResultAnd[results.Result|_RhsResult]":
        return named_result_and.NamedResultAnd[results.Result | _RhsResult]([self, rhs])

    @overload
    def __or__(
        self, rhs: "no_result_rule.NoResultRule[results.Result]"
    ) -> "named_result_or.NamedResultOr[results.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "single_result_rule.SingleResultRule[results.Result]"
    ) -> "named_result_or.NamedResultOr[results.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_result_rule.OptionalResultRule[results.Result]"
    ) -> "named_result_or.NamedResultOr[results.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "multiple_result_rule.MultipleResultRule[results.Result]"
    ) -> "named_result_or.NamedResultOr[results.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "NamedResultRule[results.Result]"
    ) -> "named_result_or.NamedResultOr[results.Result]":
        ...

    def __or__(
        self, rhs: "or_args.OrArgs[results.Result]"
    ) -> "or_.Or[results.Result,rule.Rule[results.Result]]":
        if isinstance(rhs, no_result_rule.NoResultRule):
            return named_result_or.NamedResultOr[results.Result]([self, rhs])
        elif isinstance(rhs, single_result_rule.SingleResultRule):
            return named_result_or.NamedResultOr[results.Result]([self, rhs])
        elif isinstance(rhs, optional_result_rule.OptionalResultRule):
            return named_result_or.NamedResultOr[results.Result]([self, rhs])
        elif isinstance(rhs, multiple_result_rule.MultipleResultRule):
            return named_result_or.NamedResultOr[results.Result]([self, rhs])
        elif isinstance(rhs, NamedResultRule):
            return named_result_or.NamedResultOr[results.Result]([self, rhs])
        else:
            raise errors.RuleError(rule=self, msg=f"unknown or rhs type {type(rhs)}")

    def convert_type(
        self,
        func: "results.NamedResultConverterFunc[results.ConverterResult]",
    ) -> "named_result_type_converter.NamedResultTypeConverter[results.Result,results.ConverterResult]":
        return named_result_type_converter.NamedResultTypeConverter[
            results.Result, results.ConverterResult
        ](self, func)

    def with_scope(
        self, scope: "scope.Scope[results.Result]"
    ) -> "NamedResultRule[results.Result]":
        return unary_named_result_rule.UnaryNamedResultRule[
            results.Result, NamedResultRule[results.Result]
        ](self, scope=scope)


from pysh.core.parser import states
from pysh.core.parser.rules import (
    scope,
    no_result_rule,
    single_result_rule,
    optional_result_rule,
    multiple_result_rule,
)
from pysh.core.parser.rules.ands import (
    and_,
    and_args,
    named_result_and,
    rand_args,
)
from pysh.core.parser.rules.literals import no_result_literal
from pysh.core.parser.rules.converters import named_result_type_converter
from pysh.core.parser.rules.ors import (
    or_,
    or_args,
    named_result_or,
)
from pysh.core.parser.rules.unary_rules import unary_named_result_rule
