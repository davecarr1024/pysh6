from dataclasses import dataclass
from pysh.core import tokens


@dataclass(frozen=True)
class Result:
    tokens: tokens.Stream
