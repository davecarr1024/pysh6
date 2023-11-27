from dataclasses import dataclass, field
from typing import (
    Any,
    Generic,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
)

_Errorable = TypeVar(
    "_Errorable",
    bound="errorable.Errorable",
)


@dataclass(kw_only=True, repr=False)
class Error(Exception, Generic[_Errorable]):
    value: _Errorable | Type[_Errorable]
    name: str
    msg: Optional[str]
    children: Sequence["Error"]
    kwargs: Mapping[str, Any]

    def _repr_line(self) -> str:
        kwargs: MutableMapping[str, Any] = dict(self.kwargs)
        if self.msg is not None:
            kwargs["msg"] = self.msg
        return f'{self.name}({self.value},{",".join(f"{key}={value}" for key, value in kwargs.items())})'

    def _repr(self, indent: int) -> str:
        s: str = f'{"  "*indent}{self._repr_line()}'
        for child in self.children:
            s += child._repr(indent + 1)
        return s

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return self._repr(0)


from . import errorable
