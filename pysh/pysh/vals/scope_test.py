from typing import MutableMapping, Optional
from unittest import TestCase
from pysh import core

from pysh.pysh import vals


class ScopeTest(TestCase):
    def test_get(self) -> None:
        for scope, name, expected in list[
            tuple[
                vals.Scope,
                str,
                Optional[vals.Val],
            ]
        ](
            [
                (
                    vals.Scope(),
                    "a",
                    None,
                ),
                (
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(vals.int_(1)),
                        }
                    ),
                    "a",
                    vals.int_(1),
                ),
                (
                    vals.Scope(
                        {},
                        vals.Scope(
                            {
                                "a": vals.Var.for_val(vals.int_(1)),
                            }
                        ),
                    ),
                    "a",
                    vals.int_(1),
                ),
                (
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(vals.int_(1)),
                        },
                        vals.Scope(
                            {
                                "a": vals.Var.for_val(vals.int_(2)),
                            }
                        ),
                    ),
                    "a",
                    vals.int_(1),
                ),
            ]
        ):
            with self.subTest(scope=scope, name=name, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        scope[name]
                else:
                    self.assertEqual(scope[name].val, expected)

    def test_set(self) -> None:
        for scope, name, val, expected in list[
            tuple[
                vals.Scope,
                str,
                vals.Val,
                vals.Scope,
            ]
        ](
            [
                (
                    vals.Scope(),
                    "a",
                    vals.int_(1),
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(vals.int_(1)),
                        }
                    ),
                ),
                (
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(vals.int_(2)),
                        }
                    ),
                    "a",
                    vals.int_(1),
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(vals.int_(1)),
                        }
                    ),
                ),
                (
                    vals.Scope(
                        {},
                        vals.Scope(
                            {
                                "a": vals.Var.for_val(vals.int_(2)),
                            }
                        ),
                    ),
                    "a",
                    vals.int_(1),
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(vals.int_(1)),
                        },
                        vals.Scope(
                            {
                                "a": vals.Var.for_val(vals.int_(2)),
                            }
                        ),
                    ),
                ),
            ]
        ):
            with self.subTest(scope=scope, name=name, val=val, expected=expected):
                scope[name] = vals.Var.for_val(val)
                self.assertEqual(scope, expected)

    def test_as_child(self) -> None:
        for scope, vars, expected in list[
            tuple[
                vals.Scope,
                MutableMapping[str, vals.Var],
                vals.Scope,
            ]
        ](
            [
                (
                    vals.Scope(),
                    {},
                    vals.Scope(
                        {},
                        vals.Scope(),
                    ),
                ),
                (
                    vals.Scope(),
                    {
                        "a": vals.Var.for_val(vals.int_(1)),
                    },
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(vals.int_(1)),
                        },
                        vals.Scope(),
                    ),
                ),
                (
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(vals.int_(1)),
                        },
                    ),
                    {
                        "a": vals.Var.for_val(vals.int_(2)),
                    },
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(vals.int_(2)),
                        },
                        vals.Scope(
                            {
                                "a": vals.Var.for_val(vals.int_(1)),
                            }
                        ),
                    ),
                ),
            ]
        ):
            with self.subTest(scope=scope, vars=vars, expected=expected):
                self.assertEqual(scope.as_child(vars), expected)

    def test_or(self) -> None:
        for lhs, rhs, expected in list[
            tuple[
                vals.Scope,
                vals.Scope,
                vals.Scope,
            ]
        ](
            [
                (
                    vals.Scope(),
                    vals.Scope(),
                    vals.Scope(),
                ),
                (
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(
                                vals.int_(1),
                            )
                        }
                    ),
                    vals.Scope(),
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(
                                vals.int_(1),
                            )
                        }
                    ),
                ),
                (
                    vals.Scope(),
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(
                                vals.int_(1),
                            )
                        }
                    ),
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(
                                vals.int_(1),
                            )
                        }
                    ),
                ),
                (
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(
                                vals.int_(2),
                            )
                        }
                    ),
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(
                                vals.int_(1),
                            )
                        }
                    ),
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(
                                vals.int_(1),
                            )
                        }
                    ),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(lhs | rhs, expected)

    def test_in(self) -> None:
        for name, scope, expected in list[
            tuple[
                str,
                vals.Scope,
                bool,
            ]
        ](
            [
                (
                    "a",
                    vals.Scope(),
                    False,
                ),
                (
                    "a",
                    vals.Scope(
                        {
                            "a": vals.Var.for_val(vals.int_(1)),
                        }
                    ),
                    True,
                ),
                (
                    "a",
                    vals.Scope(
                        {},
                        vals.Scope(
                            {
                                "a": vals.Var.for_val(vals.int_(1)),
                            }
                        ),
                    ),
                    True,
                ),
            ]
        ):
            with self.subTest(name=name, scope=scope, expected=expected):
                self.assertEqual(name in scope, expected)
