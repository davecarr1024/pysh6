from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, overload
from pysh.core import lexer
from pysh.core.parser import errors, results
from pysh.core.parser.rules import rule
from pysh.core.parser.rules.converters import converter_result


@dataclass(frozen=True)
class OptionalResultRule(rule.Rule[results.Result]):
    @abstractmethod
    def __call__(
        self, state: "states.State[results.Result]"
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

    def convert(
        self,
        func: "optional_result_converter.OptionalResultConverterFunc[results.Result, converter_result.ConverterResult]",
    ) -> "optional_result_converter.OptionalResultConverter[results.Result,converter_result.ConverterResult]":
        return optional_result_converter.OptionalResultConverter[
            results.Result, converter_result.ConverterResult
        ](self, func)


from pysh.core.parser import states
from pysh.core.parser.rules import (
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
