from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, overload
from pysh.core import lexer
from pysh.core.parser import errors, results
from pysh.core.parser.rules import rule


@dataclass(frozen=True)
class OptionalResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: "states.State", scope: "scope.Scope[results.Result]"
    ) -> "states.StateAndOptionalResult[results.Result]":
        ...

    def optional(self) -> "OptionalResultRule[results.Result]":
        return self

    def single(self) -> "single_result_rule.SingleResultRule[results.Result]":
        raise errors.RuleError(
            rule=self, msg="unable to convert OptionalResultRule to SingleResultRule"
        )

    @overload
    def __and__(
        self, rhs: "no_result_rule.NoResultRule[results.Result]"
    ) -> "optional_result_and.OptionalResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "single_result_rule.SingleResultRule[results.Result]"
    ) -> "multiple_result_and.MultipleResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "OptionalResultRule[results.Result]"
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
    def __and__(
        self, rhs: str
    ) -> "optional_result_and.OptionalResultAnd[results.Result]":
        ...

    @overload
    def __and__(
        self, rhs: "lexer.Rule"
    ) -> "optional_result_and.OptionalResultAnd[results.Result]":
        ...

    def __and__(
        self, rhs: "and_args.AndArgs"
    ) -> "and_.And[results.Result, rule.Rule[results.Result]]":
        if isinstance(rhs, no_result_rule.NoResultRule):
            return optional_result_and.OptionalResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, single_result_rule.SingleResultRule):
            return multiple_result_and.MultipleResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, OptionalResultRule):
            return multiple_result_and.MultipleResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, multiple_result_rule.MultipleResultRule):
            return multiple_result_and.MultipleResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, named_result_rule.NamedResultRule):
            return named_result_and.NamedResultAnd[results.Result]([self, rhs])
        elif isinstance(rhs, str) or isinstance(rhs, lexer.Rule):
            return optional_result_and.OptionalResultAnd[results.Result](
                [
                    self,
                    no_result_literal.NoResultLiteral[results.Result].load(rhs),
                ]
            )
        else:
            raise errors.RuleError(rule=self, msg=f"unknown and rhs type {type(rhs)}")

    @overload
    def __rand__(
        self, lhs: str
    ) -> "optional_result_and.OptionalResultAnd[results.Result]":
        ...

    @overload
    def __rand__(
        self, lhs: "lexer.Rule"
    ) -> "optional_result_and.OptionalResultAnd[results.Result]":
        ...

    def __rand__(
        self, lhs: "rand_args.RandArgs"
    ) -> "optional_result_and.OptionalResultAnd[results.Result]":
        return no_result_literal.NoResultLiteral[results.Result].load(lhs) & self

    @overload
    def __or__(
        self, rhs: "no_result_rule.NoResultRule[results.Result]"
    ) -> "optional_result_or.OptionalResultOr[results.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "single_result_rule.SingleResultRule[results.Result]"
    ) -> "optional_result_or.OptionalResultOr[results.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "OptionalResultRule[results.Result]"
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
        elif isinstance(rhs, single_result_rule.SingleResultRule):
            return optional_result_or.OptionalResultOr[results.Result]([self, rhs])
        elif isinstance(rhs, OptionalResultRule):
            return optional_result_or.OptionalResultOr[results.Result]([self, rhs])
        elif isinstance(rhs, multiple_result_rule.MultipleResultRule):
            return multiple_result_or.MultipleResultOr[results.Result]([self, rhs])
        elif isinstance(rhs, named_result_rule.NamedResultRule):
            return named_result_or.NamedResultOr[results.Result]([self, rhs])
        else:
            raise errors.RuleError(rule=self, msg=f"unknown or rhs type {type(rhs)}")

    def convert(
        self,
        func: "results.OptionalResultConverterFunc[results.Result, results.ConverterResult]",
    ) -> "optional_result_converter.OptionalResultConverter[results.Result,results.ConverterResult]":
        return optional_result_converter.OptionalResultConverter[
            results.Result, results.ConverterResult
        ](self, func)

    def with_scope(
        self, scope: "scope.Scope[results.Result]"
    ) -> "OptionalResultRule[results.Result]":
        return unary_optional_result_rule.UnaryOptionalResultRule[
            results.Result, OptionalResultRule[results.Result]
        ](self, scope=scope)


from pysh.core.parser import states
from pysh.core.parser.rules import (
    scope,
    no_result_rule,
    single_result_rule,
    multiple_result_rule,
    named_result_rule,
)
from pysh.core.parser.rules.ands import (
    and_,
    and_args,
    optional_result_and,
    multiple_result_and,
    named_result_and,
    rand_args,
)
from pysh.core.parser.rules.literals import no_result_literal
from pysh.core.parser.rules.converters import optional_result_converter
from pysh.core.parser.rules.ors import (
    or_,
    or_args,
    optional_result_or,
    multiple_result_or,
    named_result_or,
)
from pysh.core.parser.rules.unary_rules import unary_optional_result_rule
