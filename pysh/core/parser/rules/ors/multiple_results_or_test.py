from dataclasses import dataclass
from typing import Optional
from unittest import TestCase
from pysh.core import errors
from pysh.core.parser import results, rules, states


class MultipleResultsOrTest(TestCase):
    def test_call(self) -> None:
        @dataclass(frozen=True)
        class State:
            ...

        def fail(_):
            raise errors.Error()

        for lhs, rhs, expected in list[
            tuple[
                rules.Rule[State, int],
                rules.Rule[State, str],
                Optional[states.StateAndMultipleResults[State, int | str]],
            ]
        ](
            [
                (
                    rules.Constant[State, int](1).convert(fail),
                    rules.Constant[State, str]("a").convert(fail),
                    None,
                ),
                (
                    rules.Constant[State, int](1).convert(fail),
                    rules.Constant[State, str]("a"),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str](["a"]),
                    ),
                ),
                (
                    rules.Constant[State, int](1),
                    rules.Constant[State, str]("a").convert(fail),
                    states.StateAndMultipleResults[State, int | str](
                        State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                rule = rules.ors.MultipleResultsOr[State, int, str]([lhs, rhs])
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(State())
                else:
                    self.assertEqual(rule(State()), expected)
