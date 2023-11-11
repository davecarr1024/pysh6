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
    def literal(value: str) -> "Regex":
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
        from pysh.core.regex import and_, any, literal, not_, or_

        @dataclass(frozen=True)
        class State:
            lexer_result: lexer.Result = field(default_factory=lexer.Result)
            scope: parser.rules.Scope["State", "_Regex"] = field(
                default_factory=lambda: _Regex.scope(),
                compare=False,
                hash=False,
                repr=False,
            )

            def __str__(self) -> str:
                return str(self.lexer_result)

            @staticmethod
            def lexer_result_setter() -> (
                parser.states.StateValueSetter["State", lexer.Result]
            ):
                return parser.states.StateValueSetter["State", lexer.Result].load(
                    lambda state: state.lexer_result,
                    lambda state, lexer_result: State(lexer_result, state.scope),
                )

            @staticmethod
            def literal(rule: str | lexer.Rule) -> parser.rules.Literal["State"]:
                if isinstance(rule, str):
                    rule = lexer.Rule(rule, Regex.literal(rule))
                return parser.rules.Literal[State](
                    State.lexer_result_setter(),
                    rule,
                )

            @staticmethod
            def scope_getter() -> (
                parser.states.StateValueGetter[
                    "State", parser.rules.Scope["State", "_Regex"]
                ]
            ):
                return parser.states.StateValueGetter[
                    "State", parser.rules.Scope["State", "_Regex"]
                ].load(lambda state: state.scope)

        @dataclass(frozen=True)
        class _Regex(parser.rules.Parsable[State, "_Regex"]):
            regex: Regex

            @classmethod
            def types(cls) -> Sequence[Type["_Regex"]]:
                return [_Regex, _Not, _Special, _Literal]

            @classmethod
            def scope_getter(
                cls,
            ) -> parser.states.StateValueGetter[
                State, parser.rules.Scope[State, "_Regex"]
            ]:
                return State.scope_getter()

            @classmethod
            def parser_rule(cls) -> parser.rules.SingleResultsRule[State, "_Regex"]:
                return parser.rules.ors.SingleResultsOr[State, _Regex, _Regex](
                    [type.ref() for type in cls.types() if type != cls]
                )

        @dataclass(frozen=True)
        class _Literal(_Regex):
            regex: literal.Literal

            @classmethod
            def parser_rule(cls) -> parser.rules.SingleResultsRule[State, "_Literal"]:
                return State.literal(
                    lexer.Rule(
                        "literal",
                        not_.Not(
                            or_.Or(
                                [
                                    literal.Literal("^"),
                                    literal.Literal("\\"),
                                ]
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
                    State.literal(
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
                return (State.literal("^").no() & _Literal.ref()).convert(
                    lambda regex: _Not(not_.Not(regex.regex))
                )

        def to_and(regexes: Sequence[_Regex]) -> Regex:
            match len(regexes):
                case 1:
                    return regexes[0].regex
                case _:
                    return and_.And([regex.regex for regex in regexes])

        rule = (
            _Regex.parser_rule()
            .until_empty(State.lexer_result_setter())
            .convert(to_and)
            .with_lexer(_Regex.lexer())
        )
        state = State(rule.lexer()(lexer.State.load(value)))
        return rule(state).results.value

    def _error(
        self,
        state: state.State,
        *,
        msg: Optional[str] = None,
        children: Sequence[errors.Error] = [],
    ) -> error.Error:
        return error.Error(regex=self, state=state, msg=msg, _children=children)
