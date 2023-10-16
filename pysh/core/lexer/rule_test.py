from typing import Optional
from unittest import TestCase
from .. import chars, regex, tokens
from . import rule, rule_error, state_and_result


class RuleTest(TestCase):
    def test_call(self):
        for rule_, state, expected in list[
            tuple[
                rule.Rule, str | chars.Stream, Optional[state_and_result.StateAndResult]
            ]
        ](
            [
                (
                    rule.Rule("r", regex.Regex.literal("ab")),
                    "ab",
                    (chars.Stream(), tokens.Token("r", "ab")),
                ),
                (
                    rule.Rule("r", regex.Regex.literal("ab")),
                    "ba",
                    None,
                ),
            ]
        ):
            with self.subTest(rule_=rule_, state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(rule_error.RuleError):
                        rule_(state)
                else:
                    actual = rule_(state)
                    self.assertEqual(
                        actual, expected, f"expectd {expected} got {actual}"
                    )

    def test_load(self):
        for rule_name, value, expected in list[tuple[str, Optional[str], rule.Rule]](
            [
                (
                    "r",
                    None,
                    rule.Rule("r", regex.Regex.literal("r")),
                ),
                (
                    "r",
                    "a",
                    rule.Rule("r", regex.Regex.literal("a")),
                ),
            ]
        ):
            with self.subTest(rule_name=rule_name, value=value, expected=expected):
                self.assertEqual(rule.Rule.load(rule_name, value), expected)
