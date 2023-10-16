from dataclasses import dataclass
from .. import chars, errors
from . import regex


@dataclass(kw_only=True)
class Error(errors.Error):
    state: chars.Stream
    regex: regex.Regex
