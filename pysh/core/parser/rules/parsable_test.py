from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Iterable, Iterator, Optional, Sequence, Sized, Type
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, rules, states


@dataclass(frozen=True)
class State:
    lexer_result: lexer.Result = field(default_factory=lexer.Result)
    scope: rules.Scope["State", "Val"] = field(
        default_factory=lambda: Val.scope(),
        compare=False,
        hash=False,
        repr=False,
    )

    def __str__(self) -> str:
        return str(self.lexer_result)

    @staticmethod
    def lexer_result_setter() -> states.StateValueSetter["State", lexer.Result]:
        return states.StateValueSetter[State, lexer.Result].load(
            lambda state: state.lexer_result,
            lambda state, lexer_result: State(lexer_result, state.scope),
        )

    @staticmethod
    def literal(lexer_rule: lexer.Rule | str) -> rules.Literal["State"]:
        if isinstance(lexer_rule, str):
            lexer_rule = lexer.Rule.load(lexer_rule)
        return rules.Literal[State](State.lexer_result_setter(), lexer_rule)

    @staticmethod
    def scope_getter() -> states.StateValueGetter["State", rules.Scope["State", "Val"]]:
        return states.StateValueGetter[State, rules.Scope[State, Val]].load(
            lambda state: state.scope
        )


@dataclass(frozen=True)
class Val(rules.Parsable[State, "Val"]):
    @classmethod
    def scope_getter(cls) -> states.StateValueGetter[State, rules.Scope[State, "Val"]]:
        return State.scope_getter()

    @classmethod
    def types(cls) -> Sequence[Type["Val"]]:
        return [Val, Int, Str, List]

    @classmethod
    def parser_rule(cls) -> rules.SingleResultsRule[State, "Val"]:
        return Int.ref() | Str.ref() | List.ref()


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


@dataclass(frozen=True)
class List(Val, Sized, Iterable[Val]):
    _values: Sequence[Val] = field(default_factory=list[Val])

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[Val]:
        return iter(self._values)

    @classmethod
    def parser_rule(cls) -> rules.SingleResultsRule[State, "List"]:
        return (
            State.literal("(").no() & Val.ref().zero_or_more() & State.literal(")").no()
        ).convert(List)


class ParsableTest(TestCase):
    def test_call(self):
        for state, expected in list[
            tuple[
                State,
                Optional[states.StateAndSingleResults[State, Val]],
            ]
        ](
            [
                (
                    State(),
                    None,
                ),
                (
                    State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("s", "b"),
                                ]
                            )
                        )
                    ),
                    None,
                ),
                (
                    State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("int", "1"),
                                ]
                            )
                        )
                    ),
                    states.StateAndSingleResults[State, Val](
                        State(),
                        results.SingleResults[Val](Int(1)),
                    ),
                ),
                (
                    State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("str", '"a"'),
                                ]
                            )
                        )
                    ),
                    states.StateAndSingleResults[State, Val](
                        State(),
                        results.SingleResults[Val](Str("a")),
                    ),
                ),
                (
                    State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("(", "("),
                                    tokens.Token(")", ")"),
                                ]
                            )
                        )
                    ),
                    states.StateAndSingleResults[State, Val](
                        State(),
                        results.SingleResults[Val](List()),
                    ),
                ),
                (
                    State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("int", "1"),
                                    tokens.Token("s", "b"),
                                ]
                            )
                        )
                    ),
                    states.StateAndSingleResults[State, Val](
                        State(
                            lexer.Result(
                                tokens.Stream(
                                    [
                                        tokens.Token("s", "b"),
                                    ]
                                )
                            )
                        ),
                        results.SingleResults[Val](Int(1)),
                    ),
                ),
                (
                    State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("str", '"a"'),
                                    tokens.Token("s", "b"),
                                ]
                            )
                        )
                    ),
                    states.StateAndSingleResults[State, Val](
                        State(
                            lexer.Result(
                                tokens.Stream(
                                    [
                                        tokens.Token("s", "b"),
                                    ]
                                )
                            )
                        ),
                        results.SingleResults[Val](Str("a")),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = Val.ref()
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    actual = rule(state)
                    self.assertEqual(
                        actual,
                        expected,
                        f"\nactual {actual} != expected {expected}",
                    )
