from unittest import TestCase
from pysh.core import lexer

from pysh.core.parser import rules


class RulesTest(TestCase):
    def test_and(self) -> None:
        no_result_rule: rules.NoResultRule[int] = rules.literals.NoResultLiteral[int](
            lexer.Rule.load("a")
        )
        single_result_rule: rules.SingleResultRule[
            int
        ] = rules.literals.SingleResultLiteral[int](
            lexer.Rule.load("a"),
            lambda token: int(token.value),
        )
        optional_result_rule: rules.OptionalResultRule[
            int
        ] = rules.literals.OptionalResultLiteral[int](
            lexer.Rule.load("a"),
            lambda token: int(token.value),
        )
        multiple_result_rule: rules.MultipleResultRule[
            int
        ] = rules.ands.MultipleResultAnd[int]([single_result_rule, single_result_rule])
        named_result_rule: rules.NamedResultRule[int] = rules.ands.NamedResultAnd[int](
            [single_result_rule.named("a"), single_result_rule.named("b")]
        )
        for lhs, rhs, expected in list[
            tuple[
                rules.Rule[int],
                rules.ands.AndArgs[int],
                rules.ands.And[int, rules.Rule[int]],
            ]
        ](
            [
                (
                    no_result_rule,
                    no_result_rule,
                    rules.ands.NoResultAnd[int]([no_result_rule, no_result_rule]),
                ),
                (
                    no_result_rule,
                    single_result_rule,
                    rules.ands.SingleResultAnd[int](
                        [no_result_rule, single_result_rule]
                    ),
                ),
                (
                    no_result_rule,
                    optional_result_rule,
                    rules.ands.OptionalResultAnd[int](
                        [no_result_rule, optional_result_rule]
                    ),
                ),
                (
                    no_result_rule,
                    multiple_result_rule,
                    rules.ands.MultipleResultAnd[int](
                        [no_result_rule, multiple_result_rule]
                    ),
                ),
                (
                    no_result_rule,
                    named_result_rule,
                    rules.ands.NamedResultAnd[int]([no_result_rule, named_result_rule]),
                ),
                (
                    single_result_rule,
                    no_result_rule,
                    rules.ands.SingleResultAnd[int](
                        [single_result_rule, no_result_rule]
                    ),
                ),
                (
                    single_result_rule,
                    single_result_rule,
                    rules.ands.MultipleResultAnd[int](
                        [single_result_rule, single_result_rule]
                    ),
                ),
                (
                    single_result_rule,
                    optional_result_rule,
                    rules.ands.MultipleResultAnd[int](
                        [single_result_rule, optional_result_rule]
                    ),
                ),
                (
                    single_result_rule,
                    multiple_result_rule,
                    rules.ands.MultipleResultAnd[int](
                        [single_result_rule, multiple_result_rule]
                    ),
                ),
                (
                    single_result_rule,
                    named_result_rule,
                    rules.ands.NamedResultAnd[int](
                        [single_result_rule, named_result_rule]
                    ),
                ),
                (
                    optional_result_rule,
                    no_result_rule,
                    rules.ands.OptionalResultAnd[int](
                        [optional_result_rule, no_result_rule]
                    ),
                ),
                (
                    optional_result_rule,
                    single_result_rule,
                    rules.ands.MultipleResultAnd[int](
                        [optional_result_rule, single_result_rule]
                    ),
                ),
                (
                    optional_result_rule,
                    optional_result_rule,
                    rules.ands.MultipleResultAnd[int](
                        [optional_result_rule, optional_result_rule]
                    ),
                ),
                (
                    optional_result_rule,
                    multiple_result_rule,
                    rules.ands.MultipleResultAnd[int](
                        [optional_result_rule, multiple_result_rule]
                    ),
                ),
                (
                    optional_result_rule,
                    named_result_rule,
                    rules.ands.NamedResultAnd[int](
                        [optional_result_rule, named_result_rule]
                    ),
                ),
                (
                    multiple_result_rule,
                    no_result_rule,
                    rules.ands.MultipleResultAnd[int](
                        [multiple_result_rule, no_result_rule]
                    ),
                ),
                (
                    multiple_result_rule,
                    single_result_rule,
                    rules.ands.MultipleResultAnd[int](
                        [multiple_result_rule, single_result_rule]
                    ),
                ),
                (
                    multiple_result_rule,
                    optional_result_rule,
                    rules.ands.MultipleResultAnd[int](
                        [multiple_result_rule, optional_result_rule]
                    ),
                ),
                (
                    multiple_result_rule,
                    multiple_result_rule,
                    rules.ands.MultipleResultAnd[int](
                        [multiple_result_rule, multiple_result_rule]
                    ),
                ),
                (
                    multiple_result_rule,
                    named_result_rule,
                    rules.ands.NamedResultAnd[int](
                        [multiple_result_rule, named_result_rule]
                    ),
                ),
                (
                    named_result_rule,
                    no_result_rule,
                    rules.ands.NamedResultAnd[int]([named_result_rule, no_result_rule]),
                ),
                (
                    named_result_rule,
                    single_result_rule,
                    rules.ands.NamedResultAnd[int](
                        [named_result_rule, single_result_rule]
                    ),
                ),
                (
                    named_result_rule,
                    optional_result_rule,
                    rules.ands.NamedResultAnd[int](
                        [named_result_rule, optional_result_rule]
                    ),
                ),
                (
                    named_result_rule,
                    multiple_result_rule,
                    rules.ands.NamedResultAnd[int](
                        [named_result_rule, multiple_result_rule]
                    ),
                ),
                (
                    named_result_rule,
                    named_result_rule,
                    rules.ands.NamedResultAnd[int](
                        [named_result_rule, named_result_rule]
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(lhs & rhs, expected)
