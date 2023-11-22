from typing import Callable, Optional
from unittest import TestCase

from pysh import core


class ErrorableTest(TestCase):
    class _Test(core.errors.Errorable["ErrorableTest._Test"]):
        def raise_error(self, msg: str) -> None:
            raise self._error(msg=msg)

        def try_(self, f: Callable[[], None]) -> None:
            self._try(f)

    def test_raise(self) -> None:
        with self.assertRaises(core.errors.Error):
            self._Test().raise_error("error")

    def test_try(self) -> None:
        def f(e: Optional[Exception] = None) -> Callable[[], None]:
            def i() -> None:
                if e:
                    raise e

            return i

        with self.assertRaises(core.errors.Error):
            self._Test().try_(f(core.errors.Error(msg="error")))
        with self.assertRaises(core.errors.Error):
            self._Test().try_(f(TypeError()))
        self._Test().try_(f())
