from unittest import TestCase
from pysh.core import lexer
from pysh.core.parser import rules


class ScopeTest(TestCase):
    def test_or(self):
        def rule(name) -> rules.SingleResultRule[int]:
            return rules.literals.SingleResultLiteral[int](
                lexer.Rule.load(name),
                lambda token: int(token.value),
            )

        for lhs, rhs, expected in list[
            tuple[
                rules.Scope[int],
                rules.Scope[int],
                rules.Scope[int],
            ]
        ](
            [
                (
                    rules.Scope[int](),
                    rules.Scope[int](),
                    rules.Scope[int](),
                ),
                (
                    rules.Scope[int](
                        {
                            "a": rule("a"),
                        }
                    ),
                    rules.Scope[int](),
                    rules.Scope[int](
                        {
                            "a": rule("a"),
                        }
                    ),
                ),
                (
                    rules.Scope[int](),
                    rules.Scope[int](
                        {
                            "a": rule("a"),
                        }
                    ),
                    rules.Scope[int](
                        {
                            "a": rule("a"),
                        }
                    ),
                ),
                (
                    rules.Scope[int](
                        {
                            "a": rule("a"),
                        }
                    ),
                    rules.Scope[int](
                        {
                            "b": rule("b"),
                        }
                    ),
                    rules.Scope[int](
                        {
                            "a": rule("a"),
                            "b": rule("b"),
                        }
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(lhs | rhs, expected)
