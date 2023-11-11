from abc import ABC, abstractmethod
from dataclasses import dataclass, field
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
    def load(value: str) -> "Regex":
        from pysh.core import lexer, parser
        from pysh.core.regex import and_, any, literal

        @dataclass(frozen=True)
        class State:
            lexer_result: lexer.Result = field(default_factory=lexer.Result)
            scope: parser.rules.Scope["State", "_Regex"] = field(
                default_factory=lambda: _Regex.scope()
            )

            @staticmethod
            def lexer_result_setter() -> (
                parser.states.StateValueSetter["State", lexer.Result]
            ):
                return parser.states.StateValueSetter["State", lexer.Result].load(
                    lambda state: state.lexer_result,
                    lambda state, lexer_result: State(lexer_result, state.scope),
                )

            @staticmethod
            def literal(value: str | lexer.Rule) -> parser.rules.Literal["State"]:
                return parser.rules.Literal[State].load(
                    State.lexer_result_setter(),
                    value,
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
                return [_Regex, _Literal]

            @classmethod
            def scope_getter(
                cls,
            ) -> parser.states.StateValueGetter[
                State, parser.rules.Scope[State, "_Regex"]
            ]:
                return State.scope_getter()

            @classmethod
            def parser_rule(cls) -> parser.rules.SingleResultsRule[State, "_Regex"]:
                return _Literal.ref()

        @dataclass(frozen=True)
        class _Literal(_Regex):
            regex: literal.Literal

            @classmethod
            def parser_rule(cls) -> parser.rules.SingleResultsRule[State, "_Literal"]:
                return State.literal(lexer.Rule("literal", any.Any())).convert(
                    lambda token: _Literal(literal.Literal(token.value))
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
