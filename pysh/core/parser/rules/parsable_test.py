from abc import abstractmethod
from dataclasses import dataclass
from typing import Sequence, Type

from pysh.core import lexer, tokens
from pysh.core.parser import rules, states


@dataclass(frozen=True)
class State:
    lexer_result: lexer.Result

    @staticmethod
    def lexer_result_setter() -> states.StateValueSetter["State", lexer.Result]:
        return states.StateValueSetter[State, lexer.Result].load(
            lambda state: state.lexer_result,
            lambda state, lexer_result: State(lexer_result),
        )

    @staticmethod
    def literal(lexer_rule: lexer.Rule | str) -> rules.Literal["State"]:
        if isinstance(lexer_rule, str):
            lexer_rule = lexer.Rule.load(lexer_rule)
        return rules.Literal[State](State.lexer_result_setter(), lexer_rule)


@dataclass(frozen=True)
class Val(rules.Parsable[State, "Val"]):
    @classmethod
    def types(cls) -> Sequence[Type["Val"]]:
        return [Val, Int, Str]

    @classmethod
    def parser_rule(cls) -> rules.SingleResultsRule[State, "Val"]:
        raise NotImplementedError()
        # return Int.ref() | Str.ref()


@dataclass(frozen=True)
class Int(Val):
    value: int

    @classmethod
    def parser_rule(cls) -> rules.SingleResultsRule[State, "Int"]:
        return State.literal(lexer.Rule.load("int", r"\d+")).convert(
            lambda token: Int(int(token.value))
        )


@dataclass(frozen=True)
class Str(Val):
    value: str

    @classmethod
    def parser_rule(cls) -> rules.SingleResultsRule[State, "Str"]:
        return State.literal(lexer.Rule.load("str", r'"(^")*"')).convert(
            lambda token: Str(token.value.strip('"'))
        )
