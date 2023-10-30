from typing import Optional
from unittest import TestCase
from pysh.core import tokens
from pysh.core import parser

from pysh.core.parser import states


class StateTest(TestCase):
    def test_head(self):
        for state, expected in list[tuple[states.State, Optional[tokens.Token]]](
            [
                (
                    states.State(),
                    None,
                ),
                (
                    states.State(tokens.Stream([tokens.Token("a", "1")])),
                    tokens.Token("a", "1"),
                ),
                (
                    states.State(
                        tokens.Stream([tokens.Token("a", "1"), tokens.Token("b", "2")])
                    ),
                    tokens.Token("a", "1"),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(parser.errors.Error):
                        state.head()
                else:
                    self.assertEqual(state.head(), expected)

    def test_tail(self):
        for state, expected in list[tuple[states.State, Optional[states.State]]](
            [
                (
                    states.State(),
                    None,
                ),
                (
                    states.State(tokens.Stream([tokens.Token("a", "1")])),
                    states.State(),
                ),
                (
                    states.State(
                        tokens.Stream([tokens.Token("a", "1"), tokens.Token("b", "2")])
                    ),
                    states.State(tokens.Stream([tokens.Token("b", "2")])),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(parser.errors.Error):
                        state.tail()
                else:
                    self.assertEqual(state.tail(), expected)
