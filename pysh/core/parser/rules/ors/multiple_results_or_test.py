from dataclasses import dataclass
from typing import Optional
from unittest import TestCase
from pysh.core import errors
from pysh.core.parser import results, rules, states


class MultipleResultsOrTest(TestCase):
    def test_call(self) -> None:
        def fail(_):
            raise errors.Error()

        for lhs, rhs, expected in list[
            tuple[
                rules.Rule[states.State, int],
                rules.Rule[states.State, str],
                Optional[states.StateAndMultipleResults[states.State, int | str]],
            ]
        ](
            [
                (
                    rules.Constant[states.State, int](1).convert(fail),
                    rules.Constant[states.State, str]("a").convert(fail),
                    None,
                ),
                (
                    rules.Constant[states.State, int](1).convert(fail),
                    rules.Constant[states.State, str]("a"),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str](["a"]),
                    ),
                ),
                (
                    rules.Constant[states.State, int](1),
                    rules.Constant[states.State, str]("a").convert(fail),
                    states.StateAndMultipleResults[states.State, int | str](
                        states.State(),
                        results.MultipleResults[int | str]([1]),
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                rule = rules.ors.MultipleResultsOr[states.State, int, str]([lhs, rhs])
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(states.State())
                else:
                    self.assertEqual(rule(states.State()), expected)
