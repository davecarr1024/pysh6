from typing import Optional
from unittest import TestCase
from pysh import core, pype


class NameTest(TestCase):
    def test_get(self) -> None:
        for lhs, scope, expected in list[
            tuple[
                pype.exprs.refs.roots.Name,
                pype.vals.Scope,
                Optional[pype.vals.Val],
            ]
        ](
            [
                (
                    pype.exprs.refs.roots.Name("a"),
                    pype.vals.Scope(),
                    None,
                ),
                (
                    pype.exprs.refs.roots.Name("a"),
                    pype.vals.Scope(
                        {
                            "a": pype.vals.builtins.Int.create(1),
                        }
                    ),
                    pype.vals.builtins.Int.create(1),
                ),
            ]
        ):
            with self.subTest((lhs, scope, expected)):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        lhs.get(scope)
                else:
                    self.assertEqual(lhs.get(scope), expected)

    def test_set(self) -> None:
        for lhs, scope, val, expected in list[
            tuple[
                pype.exprs.refs.roots.Name,
                pype.vals.Scope,
                pype.vals.Val,
                pype.vals.Scope,
            ]
        ](
            [
                (
                    pype.exprs.refs.roots.Name("a"),
                    pype.vals.Scope(),
                    pype.vals.builtins.Int.create(1),
                    pype.vals.Scope(
                        {
                            "a": pype.vals.builtins.Int.create(1),
                        }
                    ),
                ),
                (
                    pype.exprs.refs.roots.Name("a"),
                    pype.vals.Scope(
                        {
                            "a": pype.vals.builtins.Int.create(1),
                        }
                    ),
                    pype.vals.builtins.Int.create(2),
                    pype.vals.Scope(
                        {
                            "a": pype.vals.builtins.Int.create(2),
                        }
                    ),
                ),
            ]
        ):
            with self.subTest((lhs, scope, val, expected)):
                lhs.set(scope, val)
                self.assertEqual(scope, expected)
