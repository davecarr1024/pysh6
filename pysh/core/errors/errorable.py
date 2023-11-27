from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Generic,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    TypeVar,
)
from pysh.core.errors import error, nary_error

_T = TypeVar(
    "_T",
    bound="Errorable",
)
_R = TypeVar("_R")


@dataclass(
    kw_only=True,
    repr=False,
)
class _Error(
    nary_error.NaryError,
    Generic[_T],
):
    name: str
    value: _T
    kwargs: Mapping[str, Any]

    def _repr_line(self) -> str:
        kwargs: MutableMapping[str, Any] = dict(self.kwargs)
        if self.msg is not None:
            kwargs["msg"] = self.msg
        return f'{self.name}({self.value},{",".join(f"{key}={value}" for key, value in kwargs.items())})'


class Errorable(Generic[_T]):
    def _error(
        self: _T,
        *,
        msg: Optional[str] = None,
        children: Optional[Sequence[error.Error]] = None,
        **kwargs: Any,
    ) -> _Error[_T]:
        return _Error[_T](
            name=self._error_name(),
            value=self,
            msg=msg,
            _children=children or [],
            kwargs=kwargs,
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
