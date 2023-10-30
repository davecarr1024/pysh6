from dataclasses import dataclass, field
from typing import Generic, Iterable, Iterator, Sequence, Sized
from pysh.core.errors import child_error, error


@dataclass(kw_only=True, repr=False)
class NaryError(
    error.Error,
    Generic[child_error.ChildError],
    Sized,
    Iterable[child_error.ChildError],
):
    _children: Sequence[child_error.ChildError] = field(
        default_factory=list[child_error.ChildError]
    )

    def __iter__(self) -> Iterator[child_error.ChildError]:
        return iter(self._children)

    def __len__(self) -> int:
        return len(self._children)

    def _repr(self, indent: int) -> str:
        s: str = super()._repr(indent)
        for child in self._children:
            s += child._repr(indent + 1)
        return s
