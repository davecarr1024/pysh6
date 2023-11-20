from dataclasses import dataclass
from typing import Callable, Generic, Optional, Sequence, TypeVar
from pysh.core.errors import error, nary_error

_T = TypeVar(
    "_T",
    bound="Errorable",
)
_R = TypeVar("_R")


class Errorable(Generic[_T]):
    def _error(
        self: _T,
        *,
        msg: Optional[str] = None,
        children: Sequence[error.Error] = [],
    ) -> error.Error:
        T = TypeVar(
            "T",
            bound=Errorable,
        )

        @dataclass(
            kw_only=True,
            repr=False,
        )
        class Error(
            Generic[T],
            nary_error.NaryError,
        ):
            name: str
            value: T

            def _repr_line(self) -> str:
                return f"{self.name}({self.value},{repr(self.msg)})"

        return Error[_T](
            name=f"{self.__class__.__name__}Error",
            value=self,
        )

    def _try(self, func: Callable[[], _R], msg: Optional[str] = None) -> _R:
        try:
            return func()
        except error.Error as error_:
            raise self._error(msg=msg, children=[error_])
        except Exception as error_:
            raise self._error(msg=f"{msg}: {error_}")
