from typing import Optional, Sequence
from unittest import TestCase
from pysh import core, pysh


class RefTest(TestCase):
    def test_create(self) -> None:
        for head, tails, expected in list[
            tuple[
                str | pysh.vals.Val,
                Sequence[str | pysh.vals.Args],
                pysh.exprs.Ref,
            ]
        ](
            [
                (
                    "a",
                    [],
                    pysh.exprs.Ref(
                        pysh.exprs.Ref.Name("a"),
                        [],
                    ),
                ),
                (
                    pysh.vals.int_(1),
                    [],
                    pysh.exprs.Ref(
                        pysh.exprs.Ref.Literal(
                            pysh.vals.int_(1),
                        ),
                        [],
                    ),
                ),
                (
                    "a",
                    [
                        "b",
                    ],
                    pysh.exprs.Ref(
                        pysh.exprs.Ref.Name("a"),
                        [
                            pysh.exprs.Ref.Member("b"),
                        ],
                    ),
                ),
                (
                    "a",
                    [
                        pysh.vals.Args(
                            [
                                pysh.vals.Arg(
                                    pysh.vals.int_(1),
                                )
                            ]
                        )
                    ],
                    pysh.exprs.Ref(
                        pysh.exprs.Ref.Name("a"),
                        [
                            pysh.exprs.Ref.Call(
                                pysh.vals.Args(
                                    [
                                        pysh.vals.Arg(
                                            pysh.vals.int_(1),
                                        )
                                    ]
                                )
                            )
                        ],
                    ),
                ),
            ]
        ):
            with self.subTest(head=head, tails=tails, expected=expected):
                self.assertEqual(pysh.exprs.Ref.create(head, *tails), expected)

    def test_eval(self) -> None:
        for ref, state, expected in list[
            tuple[
                pysh.exprs.Ref,
                pysh.State,
                Optional[pysh.vals.Val],
            ]
        ](
            [
                (
                    pysh.exprs.literal(pysh.vals.int_(1)),
                    pysh.State(),
                    pysh.vals.int_(1),
                ),
                (
                    pysh.exprs.ref_("a"),
                    pysh.State(),
                    None,
                ),
                (
                    pysh.exprs.ref_("a"),
                    pysh.State(
                        pysh.vals.Scope(
                            {
                                "a": pysh.vals.Var.for_val(pysh.vals.int_(1)),
                            }
                        )
                    ),
                    pysh.vals.int_(1),
                ),
            ]
        ):
            with self.subTest(ref=ref, state=state, expected=expected):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        ref.eval(state)
                else:
                    self.assertEqual(ref.eval(state), expected)

    def test_set(self) -> None:
        for ref, state, val, expected in list[
            tuple[
                pysh.exprs.Ref,
                pysh.State,
                pysh.vals.Val,
                Optional[pysh.State],
            ]
        ](
            [
                (
                    pysh.exprs.literal(pysh.vals.int_(1)),
                    pysh.State(),
                    pysh.vals.int_(2),
                    None,
                ),
                (
                    pysh.exprs.ref_("a"),
                    pysh.State(),
                    pysh.vals.int_(1),
                    None,
                ),
                (
                    pysh.exprs.ref_("a"),
                    pysh.State(
                        pysh.vals.Scope(
                            {
                                "a": pysh.vals.Var.for_val(
                                    pysh.vals.none,
                                ),
                            }
                        )
                    ),
                    pysh.vals.int_(1),
                    None,
                ),
                (
                    pysh.exprs.ref_("a"),
                    pysh.State(
                        pysh.vals.Scope(
                            {
                                "a": pysh.vals.Var(
                                    pysh.vals.int_class,
                                ),
                            }
                        )
                    ),
                    pysh.vals.int_(1),
                    pysh.State(
                        pysh.vals.Scope(
                            {
                                "a": pysh.vals.Var.for_val(
                                    pysh.vals.int_(1),
                                ),
                            }
                        )
                    ),
                ),
                (
                    pysh.exprs.ref_("a"),
                    pysh.State(
                        pysh.vals.Scope(
                            {
                                "a": pysh.vals.Var.for_val(
                                    pysh.vals.int_(2),
                                ),
                            }
                        )
                    ),
                    pysh.vals.int_(1),
                    pysh.State(
                        pysh.vals.Scope(
                            {
                                "a": pysh.vals.Var.for_val(
                                    pysh.vals.int_(1),
                                ),
                            }
                        )
                    ),
                ),
            ]
        ):
            with self.subTest((ref, state, val, expected)):
                if expected is None:
                    with self.assertRaises(core.errors.Error):
                        ref.set(state, val)
                else:
                    ref.set(state, val)
                    self.assertEqual(
                        state,
                        expected,
                        f"actual {state} != expected {expected}",
                    )
