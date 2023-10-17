from dataclasses import dataclass
from pysh.core import chars, errors
from pysh.core.regex import regex


@dataclass(kw_only=True)
class Error(errors.Error):
    state: chars.Stream
    regex: regex.Regex
