from dataclasses import dataclass
from . import regex


@dataclass(frozen=True)
class UnaryRegex(regex.Regex):
    child: regex.Regex
