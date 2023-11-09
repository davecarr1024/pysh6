from typing import Optional
from unittest import TestCase
from pysh.core import chars, errors, lexer, regex, tokens


class RuleTest(TestCase):
    def test_load(self):
        for name, regex_, expected in list[
            tuple[
                str,
                str | regex.Regex | None,
                lexer.Rule,
            ]
        ](
            [
                (
                    "a",
                    None,
                    lexer.Rule("a", regex.Literal("a")),
                ),
                (
                    "a",
                    "b",
                    lexer.Rule("a", regex.Literal("b")),
                ),
                (
                    "a",
                    regex.Or([regex.Literal("b"), regex.Literal("c")]),
                    lexer.Rule("a", regex.Or([regex.Literal("b"), regex.Literal("c")])),
                ),
            ]
        ):
            with self.subTest(name=name, regex_=regex_, expected=expected):
                self.assertEqual(lexer.Rule.load(name, regex_), expected)

    def test_call(self):
        for state, expected in list[
            tuple[
                lexer.State,
                Optional[lexer.StateAndResult],
            ]
        ](
            [
                (
                    lexer.State(),
                    None,
                ),
                (
                    lexer.State.load("a"),
                    lexer.StateAndResult(
                        lexer.State(),
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("r", "a"),
                                ]
                            )
                        ),
                    ),
                ),
                (
                    lexer.State.load("ab"),
                    lexer.StateAndResult(
                        lexer.State.load("b", chars.Position(0, 1)),
                        lexer.Result(
                            tokens.Stream(
                                [
                                    tokens.Token("r", "a"),
                                ]
                            )
                        ),
                    ),
                ),
            ]
        ):
            with self.subTest(state=state, expected=expected):
                rule = lexer.Rule.load("r", "a")
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state)
                else:
                    self.assertEqual(rule(state), expected)
