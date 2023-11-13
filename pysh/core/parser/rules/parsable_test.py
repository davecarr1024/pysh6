from dataclasses import dataclass, field
from typing import Iterable, Iterator, Optional, Sequence, Sized, Type
from unittest import TestCase
from pysh.core import errors, lexer, tokens
from pysh.core.parser import results, rules, states

_scope_getter: states.StateValueGetter[
    "State", rules.Scope["State", "Val"]
] = states.StateValueGetter["State", rules.Scope["State", "Val"]].load(
    lambda state: state.scope
)


@dataclass(frozen=True)
class State(states.State):
    scope: rules.Scope["State", "Val"] = field(
        default_factory=lambda: Val.scope(),
        compare=False,
        hash=False,
        repr=False,
    )

    def with_lexer_result(self, lexer_result: lexer.Result) -> "State":
        return State(lexer_result, self.scope)

    @staticmethod
    def scope_getter() -> states.StateValueGetter["State", rules.Scope["State", "Val"]]:
        return _scope_getter


@dataclass(frozen=True)
class Val(rules.Parsable[State, "Val"]):
    @classmethod
    def scope_getter(cls) -> states.StateValueGetter[State, rules.Scope[State, "Val"]]:
        return State.scope_getter()

    @classmethod
    def types(cls) -> Sequence[Type["Val"]]:
        return [cls, Int, Str, List]


@dataclass(frozen=True)
class Int(Val):
    value: int

    @classmethod
    def parser_rule(cls) -> rules.SingleResultsRule[State, "Int"]:
        return rules.Literal[State](lexer.Rule.load("int", r"\d+")).convert(
            lambda token: Int(int(token.value))
        )


@dataclass(frozen=True)
class Str(Val):
    value: str

    @classmethod
    def parser_rule(cls) -> rules.SingleResultsRule[State, "Str"]:
        return rules.Literal[State](lexer.Rule.load("str", r'"(^")*"')).convert(
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
            rules.Literal[State](lexer.Rule.load(r"\(")).no()
            & Val.ref().until(rules.Literal[State](lexer.Rule.load(r"\)")).no())
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
                (
                    State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token(r"\(", "("),
                                    tokens.Token(r"\)", ")"),
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
                                    tokens.Token(r"\(", "("),
                                    tokens.Token("int", "1"),
                                    tokens.Token(r"\)", ")"),
                                ]
                            )
                        )
                    ),
                    states.StateAndSingleResults[State, Val](
                        State(),
                        results.SingleResults[Val](List([Int(1)])),
                    ),
                ),
                (
                    State(
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token(r"\(", "("),
                                    tokens.Token("str", '"a"'),
                                    tokens.Token(r"\)", ")"),
                                ]
                            )
                        )
                    ),
                    states.StateAndSingleResults[State, Val](
                        State(),
                        results.SingleResults[Val](List([Str("a")])),
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
