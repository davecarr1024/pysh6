from dataclasses import dataclass
from .. import stream


@dataclass(frozen=True)
class Stream(stream.Stream['token.Token']):
    ...

from . import token