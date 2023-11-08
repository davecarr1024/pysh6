# from typing import Optional
# from unittest import TestCase
# from pysh.core import chars, errors, regex


# class RegexTest(TestCase):
#     def test_literal(self):
#         for value, expected in list[tuple[str, Optional[regex.Regex]]](
#             [
#                 (
#                     "",
#                     regex.And([]),
#                 ),
#                 (
#                     "a",
#                     regex.Literal("a"),
#                 ),
#                 (
#                     "ab",
#                     regex.And(
#                         [
#                             regex.Literal("a"),
#                             regex.Literal("b"),
#                         ]
#                     ),
#                 ),
#             ]
#         ):
#             with self.subTest(value=value, expected=expected):
#                 self.assertEqual(regex.Regex.literal(value), expected)

#     def test_call(self):
#         for regex_, state, expected in list[
#             tuple[regex.Regex, chars.Stream | str, Optional[regex.StateAndResult | str]]
#         ](
#             [
#                 (
#                     regex.Any(),
#                     "a",
#                     "a",
#                 ),
#                 (
#                     regex.Any(),
#                     "",
#                     None,
#                 ),
#                 (
#                     regex.Literal("a"),
#                     "a",
#                     "a",
#                 ),
#                 (
#                     regex.Literal("a"),
#                     "",
#                     None,
#                 ),
#                 (
#                     regex.Literal("a"),
#                     "b",
#                     None,
#                 ),
#                 (
#                     regex.And([regex.Literal("a"), regex.Literal("b")]),
#                     "",
#                     None,
#                 ),
#                 (
#                     regex.And([regex.Literal("a"), regex.Literal("b")]),
#                     "a",
#                     None,
#                 ),
#                 (
#                     regex.And([regex.Literal("a"), regex.Literal("b")]),
#                     "b",
#                     None,
#                 ),
#                 (
#                     regex.And([regex.Literal("a"), regex.Literal("b")]),
#                     "ab",
#                     "ab",
#                 ),
#                 (
#                     regex.Or([regex.Literal("a"), regex.Literal("b")]),
#                     "",
#                     None,
#                 ),
#                 (
#                     regex.Or([regex.Literal("a"), regex.Literal("b")]),
#                     "c",
#                     None,
#                 ),
#                 (
#                     regex.Or([regex.Literal("a"), regex.Literal("b")]),
#                     "a",
#                     "a",
#                 ),
#                 (
#                     regex.Or([regex.Literal("a"), regex.Literal("b")]),
#                     "b",
#                     "b",
#                 ),
#                 (
#                     regex.OneOrMore(regex.Literal("a")),
#                     "",
#                     None,
#                 ),
#                 (
#                     regex.OneOrMore(regex.Literal("a")),
#                     "a",
#                     "a",
#                 ),
#                 (
#                     regex.OneOrMore(regex.Literal("a")),
#                     "aa",
#                     "aa",
#                 ),
#                 (
#                     regex.ZeroOrMore(regex.Literal("a")),
#                     "",
#                     "",
#                 ),
#                 (
#                     regex.ZeroOrMore(regex.Literal("a")),
#                     "a",
#                     "a",
#                 ),
#                 (
#                     regex.ZeroOrMore(regex.Literal("a")),
#                     "aa",
#                     "aa",
#                 ),
#                 (
#                     regex.ZeroOrOne(regex.Literal("a")),
#                     "",
#                     "",
#                 ),
#                 (
#                     regex.ZeroOrOne(regex.Literal("a")),
#                     "a",
#                     "a",
#                 ),
#                 (
#                     regex.ZeroOrOne(regex.Literal("a")),
#                     "b",
#                     (
#                         chars.Stream.load("b"),
#                         regex.Result.load(""),
#                     ),
#                 ),
#                 (
#                     regex.ZeroOrOne(regex.Literal("a")),
#                     "aa",
#                     (
#                         chars.Stream([chars.Char("a", chars.Position(0, 1))]),
#                         regex.Result.load("a"),
#                     ),
#                 ),
#             ]
#         ):
#             with self.subTest(regex=regex_, state=state, expected=expected):
#                 if isinstance(state, str):
#                     state = chars.Stream.load(state)
#                 if expected is None:
#                     with self.assertRaises(errors.Error):
#                         regex_(state)
#                 else:
#                     if isinstance(expected, str):
#                         expected = (chars.Stream(), regex.Result.load(expected))
#                     actual = regex_(state)
#                     self.assertEqual(
#                         actual,
#                         expected,
#                         f"actual {str(actual)} != expected {str(expected)}",
#                     )
