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
        T = TypeVar("T", bound=Errorable)

        @dataclass(
            kw_only=True,
            repr=False,
        )
        class Error(
            nary_error.NaryError,
            Generic[T],
        ):
            name: str
            value: T

            def _repr_line(self) -> str:
                return (
                    f"{self.name}({self.value},{repr(self.msg)})"
                    if self.msg is not None
                    else f"{self.name}({self.value})"
                )

        return Error(
            name=self._error_name(),
            value=self,
            msg=msg,
            _children=children,
        )

    def _error_name(self) -> str:
        return f"{self.__class__.__name__}.Error"

    def _try(self, func: Callable[[], _R], msg: Optional[str] = None) -> _R:
        try:
            return func()
        except error.Error as error_:
            raise self._error(msg=msg, children=[error_])
        except Exception as error_:
            raise self._error(msg=f"{msg}: {error_}")
