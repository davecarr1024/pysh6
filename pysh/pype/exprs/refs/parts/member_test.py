from typing import Optional
from unittest import TestCase
from pysh import core, pype


class MemberTest(TestCase):
    def test_get(self) -> None:
        for lhs, obj, expected in list[
            tuple[
                pype.exprs.refs.parts.Member,
                pype.vals.Val,
                Optional[pype.vals.Val],
            ]
        ](
            [
                (
                    pype.exprs.refs.parts.Member("a"),
                    pype.vals.builtins.Int.create(1),
                    None,
                ),
                (
                    pype.exprs.refs.parts.Member("a"),
                    pype.vals.classes.Class(
                        _name="c",
                        members=pype.vals.Scope(
                            {
                                "a": pype.vals.builtins.Int.create(1),
                            }
                        ),
                    ),
                    pype.vals.builtins.Int.create(1),
                ),
            ]
        ):
            with self.subTest((lhs, obj, expected)):
                scope = pype.vals.Scope()
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        lhs.get(scope, obj)
                else:
                    self.assertEqual(lhs.get(scope, obj), expected)

    def test_set(self) -> None:
        for lhs, obj, val, expected in list[
            tuple[
                pype.exprs.refs.parts.Member,
                pype.vals.Val,
                pype.vals.Val,
                pype.vals.Val,
            ]
        ](
            [
                (
                    pype.exprs.refs.parts.Member("a"),
                    pype.vals.classes.Class(_name="c"),
                    pype.vals.builtins.Int.create(1),
                    pype.vals.classes.Class(
                        _name="c",
                        members=pype.vals.Scope(
                            {
                                "a": pype.vals.builtins.Int.create(1),
                            }
                        ),
                    ),
                ),
            ]
        ):
            with self.subTest((lhs, obj, val, expected)):
                scope = pype.vals.Scope()
                lhs.set(scope, obj, val)
                self.assertEqual(obj, expected)
