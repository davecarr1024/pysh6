from unittest import TestCase
from pysh.core import lexer, tokens
from pysh.core.parser import rules, states


class LiteralTest(TestCase):
    def test_call(self):
        rule = rules.Literal[tokens.Stream](
            states.StateSelfExtractor[tokens.Stream](),
            lexer.Rule.load("a"),
        )
