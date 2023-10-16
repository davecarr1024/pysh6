from dataclasses import dataclass
from .. import chars, errors
from . import regex


@dataclass(frozen=True, kw_only=True)
class Error(errors.NaryError):
    state: chars.Stream
    regex: regex.Regex
