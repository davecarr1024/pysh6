from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import string
from typing import Optional, Sequence, Type
from pysh.core import errors
from pysh.core.regex import error, state, state_and_result


class Regex(ABC):
    @abstractmethod
    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        ...

    @staticmethod
    def _literal(value: str) -> "Regex":
        from pysh.core.regex import and_, literal

        literals = [literal.Literal(c) for c in value]
        if len(literals) == 1:
            return literals[0]
        return and_.And(literals)

    @staticmethod
    def _or(values: Sequence[str]) -> "Regex":
        from pysh.core.regex import literal, or_

        return or_.Or([literal.Literal(value) for value in values])

    @staticmethod
    def digits() -> "Regex":
        return Regex._or(string.digits)

    @staticmethod
    def whitespace() -> "Regex":
        return Regex._or(string.whitespace)

    @staticmethod
    def load(value: str) -> "Regex":
        from pysh.core import lexer, parser
        from pysh.core.regex import (
            and_,
            any,
            literal,
            not_,
            one_or_more,
            or_,
            range,
            zero_or_more,
            zero_or_one,
        )

        scope_getter = parser.states.StateValueGetter[
            "State", parser.rules.Scope["State", "_Regex"]
        ].load(lambda state: state.scope)

        @dataclass(frozen=True)
        class State(parser.states.State):
            scope: parser.rules.Scope["State", "_Regex"] = field(
                default_factory=lambda: _Regex.parser_scope(),
                compare=False,
                hash=False,
                repr=False,
            )

            def with_lexer_result(self, lexer_result: lexer.Result) -> "State":
                return State(lexer_result, self.scope)

        def _literal(value: str | lexer.Rule) -> parser.rules.Literal[State]:
            if isinstance(value, str):
                value = lexer.Rule(value, Regex._literal(value))
            return parser.rules.Literal[State](value)

        @dataclass(frozen=True)
        class _Regex(parser.Parsable[State, "_Regex"]):
            regex: Regex

            @classmethod
            def types(cls) -> Sequence[Type["_Regex"]]:
                return [
                    cls,
                    _ZeroOrMore,
                    _OneOrMore,
                    _ZeroOrOne,
                    _Literal,
                    _Not,
                    _Special,
                    _Range,
                    _Any,
                    _And,
                    _Or,
                ]

            @classmethod
            def scope_getter(
                cls,
            ) -> parser.states.StateValueGetter[
                State, parser.rules.Scope[State, "_Regex"]
            ]:
                return scope_getter

        @dataclass(frozen=True)
        class _Literal(_Regex):
            regex: literal.Literal

            @classmethod
            def parser_rule(cls) -> parser.rules.SingleResultsRule[State, "_Literal"]:
                return _literal(
                    lexer.Rule(
                        "literal",
                        not_.Not(
                            or_.Or(
                                [literal.Literal(value) for value in r"\^[-].(|)*?+"]
                            )
                        ),
                    )
                ).convert(lambda token: _Literal(literal.Literal(token.value)))

        @dataclass(frozen=True)
        class _Special(_Regex):
            regex: Regex

            @classmethod
            def parser_rule(cls) -> parser.rules.SingleResultsRule[State, "_Special"]:
                def special(value: str) -> _Special:
                    match value:
                        case "d":
                            return _Special(Regex.digits())
                        case "s":
                            return _Special(Regex.whitespace())
                        case _:
                            return _Special(literal.Literal(value))

                return (
                    _literal(
                        lexer.Rule(
                            "special", and_.And([literal.Literal("\\"), any.Any()])
                        )
                    )
                    .token_value()
                    .convert(lambda value: value[1:])
                    .convert(special)
                )

        @dataclass(frozen=True)
        class _Not(_Regex):
            regex: not_.Not

            @classmethod
            def parser_rule(cls) -> parser.rules.SingleResultsRule[State, "_Not"]:
                return (_literal("^").no() & (_Literal.ref() | _Range.ref())).convert(
                    lambda regex: _Not(not_.Not(regex.regex))
                )

        @dataclass(frozen=True)
        class _Range(_Regex):
            regex: range.Range

            @classmethod
            def parser_rule(cls) -> parser.rules.SingleResultsRule[State, "_Range"]:
                return (
                    _literal(
                        lexer.Rule(
                            "range",
                            and_.And(
                                [
                                    literal.Literal("["),
                                    any.Any(),
                                    literal.Literal("-"),
                                    any.Any(),
                                    literal.Literal("]"),
                                ]
                            ),
                        )
                    )
                    .token_value()
                    .convert(
                        lambda value: _Range(range.Range(*value.strip("[]").split("-")))
                    )
                )

        @dataclass(frozen=True)
        class _Any(_Regex):
            regex: any.Any = field(default_factory=any.Any)

            @classmethod
            def parser_rule(cls) -> parser.rules.SingleResultsRule[State, "_Any"]:
                return _literal(".").no().convert(lambda: _Any())

        @dataclass(frozen=True)
        class _And(_Regex):
            regex: Regex

            @classmethod
            def parser_rule(cls) -> parser.rules.SingleResultsRule[State, "_And"]:
                def load(regexes: Sequence[_Regex]) -> _And:
                    values = [regex.regex for regex in regexes]
                    match len(values):
                        case 1:
                            return _And(values[0])
                        case _:
                            return _And(and_.And(values))

                return (
                    _literal("(").no()
                    & _Regex.ref().one_or_more().until(_literal(")").no())
                ).convert(load)

        @dataclass(frozen=True)
        class _Or(_Regex):
            regex: or_.Or

            @classmethod
            def parser_rule(cls) -> parser.rules.SingleResultsRule[State, "_Or"]:
                return (
                    _literal("(").no()
                    & _Regex.ref()
                    & (_literal("|").no() & _Regex.ref())
                    .one_or_more()
                    .until(_literal(")").no())
                ).convert(
                    lambda regexes: _Or(or_.Or([regex.regex for regex in regexes]))
                )

        @dataclass(frozen=True)
        class _ZeroOrMore(_Regex):
            regex: zero_or_more.ZeroOrMore

            @classmethod
            def parser_rule(
                cls,
            ) -> parser.rules.SingleResultsRule[State, "_ZeroOrMore"]:
                return (
                    (
                        _Literal.ref()
                        | _And.ref()
                        | _Or.ref()
                        | _Range.ref()
                        | _Any.ref()
                        | _Special.ref()
                    )
                    & _literal("*").no()
                ).convert(
                    lambda regex: _ZeroOrMore(zero_or_more.ZeroOrMore(regex.regex))
                )

        @dataclass(frozen=True)
        class _OneOrMore(_Regex):
            regex: one_or_more.OneOrMore

            @classmethod
            def parser_rule(
                cls,
            ) -> parser.rules.SingleResultsRule[State, "_OneOrMore"]:
                return (
                    (
                        _Literal.ref()
                        | _And.ref()
                        | _Or.ref()
                        | _Range.ref()
                        | _Any.ref()
                        | _Special.ref()
                    )
                    & _literal("+").no()
                ).convert(lambda regex: _OneOrMore(one_or_more.OneOrMore(regex.regex)))

        @dataclass(frozen=True)
        class _ZeroOrOne(_Regex):
            regex: zero_or_one.ZeroOrOne

            @classmethod
            def parser_rule(
                cls,
            ) -> parser.rules.SingleResultsRule[State, "_ZeroOrOne"]:
                return (
                    (
                        _Literal.ref()
                        | _And.ref()
                        | _Or.ref()
                        | _Range.ref()
                        | _Any.ref()
                        | _Special.ref()
                    )
                    & _literal("?").no()
                ).convert(lambda regex: _ZeroOrOne(zero_or_one.ZeroOrOne(regex.regex)))

        def to_and(regexes: Sequence[_Regex]) -> Regex:
            match len(regexes):
                case 1:
                    return regexes[0].regex
                case _:
                    return and_.And([regex.regex for regex in regexes])

        rule = _Regex.ref().until_empty().convert(to_and).with_lexer(_Regex.lexer())
        state = State(rule.lexer()(lexer.State.load(value)))
        try:
            return rule(state).results.value
        except errors.Error as error_:
            raise errors.UnaryError(
                msg=f"failed to load regex {repr(value)}", child=error_
            )

    def _error(
        self,
        state: state.State,
        *,
        msg: Optional[str] = None,
        children: Sequence[errors.Error] = [],
    ) -> error.Error:
        return error.Error(regex=self, state=state, msg=msg, _children=children)
