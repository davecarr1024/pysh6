from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, Optional, overload
from pysh.core import lexer
from pysh.core.parser import errors, results
from pysh.core.parser.rules import rule
from pysh.core.parser.rules.converters import converter_result


@dataclass(frozen=True)
class NamedResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: "states.State[results.Result]"
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

    def convert(
        self,
        func: "named_result_converter.NamedResultConverterFunc[results.Result, converter_result.ConverterResult]",
    ) -> "named_result_converter.NamedResultConverter[results.Result,converter_result.ConverterResult]":
        return named_result_converter.NamedResultConverter[
            results.Result, converter_result.ConverterResult
        ](self, func)


from pysh.core.parser import states
from pysh.core.parser.rules import (
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
from pysh.core.parser.rules.converters import named_result_converter
