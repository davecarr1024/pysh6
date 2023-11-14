from dataclasses import dataclass
from unittest import TestCase
from pysh.core import lexer
from pysh.core.parser import results, rules, states


class NamedResultsAndTest(TestCase):
    def test_call(self) -> None:
        @dataclass(frozen=True)
        class State(states.State):
            def with_lexer_result(self, lexer_result: lexer.Result) -> "State":
                return State(lexer_result)

        for lhs, rhs, expected in list[
            tuple[
                rules.Rule[State, int] | rules.Rule[State, str],
                rules.Rule[State, int] | rules.Rule[State, str],
                states.StateAndNamedResults[State, int | str],
            ]
        ](
            [
                (
                    rules.Constant[State, int](1).no().named(),
                    rules.Constant[State, int](2).no(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().named(),
                    rules.Constant[State, int](2),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"": 2}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().named(),
                    rules.Constant[State, int](2).no().optional(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().named(),
                    rules.Constant[State, int](2).optional(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"": 2}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().named(),
                    rules.Constant[State, int](2).no().named(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().named(),
                    rules.Constant[State, int](2).named(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"": 2}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().named(),
                    rules.Constant[State, int](2).no().named(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str](),
                    ),
                ),
                (
                    rules.Constant[State, int](1).no().named(),
                    rules.Constant[State, int](2).named(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"": 2}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).named("a"),
                    rules.Constant[State, int](2).no(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"a": 1}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).named("a"),
                    rules.Constant[State, int](2),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"a": 1, "": 2}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).named("a"),
                    rules.Constant[State, int](2).no().optional(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"a": 1}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).named("a"),
                    rules.Constant[State, int](2).optional(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"a": 1, "": 2}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).named("a"),
                    rules.Constant[State, int](2).no().multiple(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"a": 1}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).named("a"),
                    rules.Constant[State, int](2).multiple(),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"a": 1, "": 2}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).named("a"),
                    rules.Constant[State, int](2).no().named("b"),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"a": 1}),
                    ),
                ),
                (
                    rules.Constant[State, int](1).named("a"),
                    rules.Constant[State, int](2).named("b"),
                    states.StateAndNamedResults[State, int | str](
                        State(),
                        results.NamedResults[int | str]({"a": 1, "b": 2}),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(
                    rules.ands.NamedResultsAnd[State, int, str]([lhs, rhs])(State()),
                    expected,
                )
