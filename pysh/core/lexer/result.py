from dataclasses import dataclass, field
from pysh.core import tokens


@dataclass(frozen=True)
class Result:
    tokens: "tokens.Stream" = field(default_factory=tokens.Stream)
