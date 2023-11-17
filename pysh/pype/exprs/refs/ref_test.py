from typing import Optional, Sequence
from unittest import TestCase
from pysh import core, pype


class RefTest(TestCase):
    def test_create(self) -> None:
        for root, parts, expected in list[
            tuple[
                str | pype.vals.Val,
                Sequence[str | pype.exprs.Args],
                pype.exprs.refs.Ref,
            ]
        ](
            [
                (
                    "a",
                    [],
                    pype.exprs.refs.Ref(
                        pype.exprs.refs.roots.Name("a"),
                    ),
                ),
                (
                    pype.vals.builtins.Int.create(1),
                    [],
                    pype.exprs.refs.Ref(
                        pype.exprs.refs.roots.Literal(
                            pype.vals.builtins.Int.create(1),
                        ),
                    ),
                ),
                (
                    "a",
                    ["b"],
                    pype.exprs.refs.Ref(
                        pype.exprs.refs.roots.Name("a"),
                        [
                            pype.exprs.refs.parts.Member("b"),
                        ],
                    ),
                ),
                (
                    "a",
                    [
                        "b",
                        pype.exprs.Args(
                            [
                                pype.exprs.Arg(
                                    pype.exprs.refs.Ref(
                                        pype.exprs.refs.roots.Literal(
                                            pype.vals.builtins.Int.create(1)
                                        )
                                    )
                                )
                            ]
                        ),
                    ],
                    pype.exprs.refs.Ref(
                        pype.exprs.refs.roots.Name("a"),
                        [
                            pype.exprs.refs.parts.Member("b"),
                            pype.exprs.refs.parts.Call(
                                pype.exprs.Args(
                                    [
                                        pype.exprs.Arg(
                                            pype.exprs.refs.Ref(
                                                pype.exprs.refs.roots.Literal(
                                                    pype.vals.builtins.Int.create(1)
                                                )
                                            )
                                        )
                                    ]
                                ),
                            ),
                        ],
                    ),
                ),
            ]
        ):
            with self.subTest(root=root, parts=parts, expected=expected):
                self.assertEqual(pype.exprs.refs.Ref.create(root, *parts), expected)

    def test_eval(self) -> None:
        for ref, scope, expected in list[
            tuple[
                pype.exprs.refs.Ref,
                pype.vals.Scope,
                Optional[pype.vals.Val],
            ]
        ](
            [
                (
                    pype.exprs.refs.Ref.create(pype.vals.builtins.Int.create(1)),
                    pype.vals.Scope(),
                    pype.vals.builtins.Int.create(1),
                ),
                (
                    pype.exprs.refs.Ref.create(
                        pype.vals.builtins.Int.create(1),
                        "a",
                    ),
                    pype.vals.Scope(),
                    None,
                ),
                (
                    pype.exprs.refs.Ref.create("a"),
                    pype.vals.Scope(),
                    None,
                ),
                (
                    pype.exprs.refs.Ref.create("a"),
                    pype.vals.Scope(
                        {
                            "a": pype.vals.builtins.Int.create(1),
                        }
                    ),
                    pype.vals.builtins.Int.create(1),
                ),
                (
                    pype.exprs.refs.Ref.create("a", "b"),
                    pype.vals.Scope(
                        {
                            "a": pype.vals.builtins.Int.create(1),
                        }
                    ),
                    None,
                ),
                (
                    pype.exprs.refs.Ref.create("a", "b"),
                    pype.vals.Scope(
                        {
                            "a": pype.vals.classes.Class(
                                _name="a",
                                members=pype.vals.Scope(
                                    {
                                        "b": pype.vals.builtins.Int.create(1),
                                    }
                                ),
                            ),
                        }
                    ),
                    pype.vals.builtins.Int.create(1),
                ),
            ]
        ):
            with self.subTest(ref=ref, scope=scope, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        ref.eval(scope)
                else:
                    self.assertEqual(ref.eval(scope), expected)

    def test_set(self) -> None:
        for ref, scope, val, expected in list[
            tuple[
                pype.exprs.refs.Ref,
                pype.vals.Scope,
                pype.vals.Val,
                pype.vals.Scope,
            ]
        ](
            [
                (
                    pype.exprs.refs.Ref.create("a"),
                    pype.vals.Scope(),
                    pype.vals.builtins.Int.create(1),
                    pype.vals.Scope(
                        {
                            "a": pype.vals.builtins.Int.create(1),
                        }
                    ),
                ),
                (
                    pype.exprs.refs.Ref.create("a", "b"),
                    pype.vals.Scope(
                        {
                            "a": pype.vals.classes.Class(
                                _name="a",
                            ),
                        }
                    ),
                    pype.vals.builtins.Int.create(1),
                    pype.vals.Scope(
                        {
                            "a": pype.vals.classes.Class(
                                _name="a",
                                members=pype.vals.Scope(
                                    {
                                        "b": pype.vals.builtins.Int.create(1),
                                    }
                                ),
                            ),
                        }
                    ),
                ),
            ]
        ):
            with self.subTest(ref=ref, scope=scope, val=val, expected=expected):
                ref.set(scope, val)
                self.assertEqual(scope, expected)
