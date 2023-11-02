from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, Optional, overload
from pysh.core import lexer
from pysh.core.parser import errors, results
from pysh.core.parser.results import converter_result
from pysh.core.parser.rules import rule


@dataclass(frozen=True)
class MultipleResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: "states.State", scope: "scope.Scope[results.Result]"
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

    @overload
    def __rand__(
        self, lhs: str
    ) -> "multiple_result_and.MultipleResultAnd[results.Result]":
        ...

    @overload
    def __rand__(
        self, lhs: "lexer.Rule"
    ) -> "multiple_result_and.MultipleResultAnd[results.Result]":
        ...

    def __rand__(
        self, lhs: "rand_args.RandArgs"
    ) -> "multiple_result_and.MultipleResultAnd[results.Result]":
        return no_result_literal.NoResultLiteral[results.Result].load(lhs) & self

    @overload
    def __or__(
        self, rhs: "no_result_rule.NoResultRule[results.Result]"
    ) -> "multiple_result_or.MultipleResultOr[results.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "single_result_rule.SingleResultRule[results.Result]"
    ) -> "multiple_result_or.MultipleResultOr[results.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "optional_result_rule.OptionalResultRule[results.Result]"
    ) -> "multiple_result_or.MultipleResultOr[results.Result]":
        ...

    @overload
    def __or__(
        self, rhs: "MultipleResultRule[results.Result]"
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
            return multiple_result_or.MultipleResultOr[results.Result]([self, rhs])
        elif isinstance(rhs, single_result_rule.SingleResultRule):
            return multiple_result_or.MultipleResultOr[results.Result]([self, rhs])
        elif isinstance(rhs, optional_result_rule.OptionalResultRule):
            return multiple_result_or.MultipleResultOr[results.Result]([self, rhs])
        elif isinstance(rhs, MultipleResultRule):
            return multiple_result_or.MultipleResultOr[results.Result]([self, rhs])
        elif isinstance(rhs, named_result_rule.NamedResultRule):
            return named_result_or.NamedResultOr[results.Result]([self, rhs])
        else:
            raise errors.RuleError(rule=self, msg=f"unknown or rhs type {type(rhs)}")

    def convert_type(
        self,
        func: "results.MultipleResultConverterFunc[results.Result, results.ConverterResult]",
    ) -> "multiple_result_type_converter.MultipleResultTypeConverter[results.Result,results.ConverterResult]":
        return multiple_result_type_converter.MultipleResultTypeConverter[
            results.Result, results.ConverterResult
        ](self, func)

    def with_scope(
        self, scope: "scope.Scope[results.Result]"
    ) -> "MultipleResultRule[results.Result]":
        return unary_multiple_result_rule.UnaryMultipleResultRule[
            results.Result, MultipleResultRule[results.Result]
        ](self, scope=scope)


from pysh.core.parser import states
from pysh.core.parser.rules import (
    scope,
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
    rand_args,
)
from pysh.core.parser.rules.literals import no_result_literal
from pysh.core.parser.rules.converters import (
    multiple_result_type_converter,
)
from pysh.core.parser.rules.ors import (
    or_,
    or_args,
    multiple_result_or,
    named_result_or,
)
from pysh.core.parser.rules.unary_rules import unary_multiple_result_rule
