from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    Sequence,
    Type,
    TypeVar,
)
from . import error

_Errorable = TypeVar(
    "_Errorable",
    bound="Errorable",
)
_R = TypeVar("_R")


class Errorable(Generic[_Errorable]):
    def _error(
        self: _Errorable,
        *,
        msg: Optional[str] = None,
        children: Optional[Sequence[error.Error]] = None,
        **kwargs: Any,
    ) -> error.Error[_Errorable]:
        return error.Error[_Errorable](
            name=self._error_name(),
            value=self,
            msg=msg,
            children=children or [],
            kwargs=kwargs,
        )

    @classmethod
    def _cls_error(
        cls: Type[_Errorable],
        *,
        msg: Optional[str] = None,
        children: Optional[Sequence[error.Error]] = None,
        **kwargs: Any,
    ) -> error.Error[_Errorable]:
        return error.Error[_Errorable](
            name=cls._error_name(),
            value=cls,
            msg=msg,
            children=children or [],
            kwargs=kwargs,
        )

    @classmethod
    def _error_name(cls) -> str:
        return f"{cls.__name__}.Error"

    def _try(
        self,
        func: Callable[[], _R],
        msg: Optional[str] = None,
        **kwargs: Any,
    ) -> _R:
        try:
            return func()
        except error.Error as error_:
            raise self._error(
                msg=msg,
                children=[error_],
                kwargs=kwargs,
            )
        except Exception as error_:
            raise self._error(
                msg=f"{msg}: {error_}",
                kwargs=kwargs,
            )

    @classmethod
    def _cls_try(
        cls: Type[_Errorable],
        func: Callable[[], _R],
        msg: Optional[str] = None,
        **kwargs: Any,
    ) -> _R:
        try:
            return func()
        except error.Error as error_:
            raise cls._cls_error(
                msg=msg,
                children=[error_],
                kwargs=kwargs,
            )
        except Exception as error_:
            raise cls._cls_error(
                msg=f"{msg}: {error_}" if msg is not None else str(error_),
                kwargs=kwargs,
            )
