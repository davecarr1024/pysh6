from dataclasses import dataclass
from pysh.core.regex import regex


@dataclass(frozen=True)
class UnaryRegex(regex.Regex):
    child: regex.Regex
