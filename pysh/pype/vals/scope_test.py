from typing import Optional
from unittest import TestCase
from pysh import core
from pysh.pype import vals


class ScopeTest(TestCase):
    def test_get(self) -> None:
        for scope, expected in list[
            tuple[
                vals.Scope,
                Optional[vals.Val],
            ]
        ](
            [
                (
                    vals.Scope(),
                    None,
                ),
                (
                    vals.Scope(
                        {
                            "a": vals.builtins.Int.create(1),
                        }
                    ),
                    vals.builtins.Int.create(1),
                ),
                (
                    vals.Scope(
                        {},
                        vals.Scope(
                            {
                                "a": vals.builtins.Int.create(1),
                            }
                        ),
                    ),
                    vals.builtins.Int.create(1),
                ),
                (
                    vals.Scope(
                        {
                            "a": vals.builtins.Int.create(1),
                        },
                        vals.Scope(
                            {
                                "a": vals.builtins.Int.create(2),
                            }
                        ),
                    ),
                    vals.builtins.Int.create(1),
                ),
            ]
        ):
            with self.subTest(scope=scope, expected=expected):
                name = "a"
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        scope[name]
                else:
                    self.assertEqual(scope[name], expected)
