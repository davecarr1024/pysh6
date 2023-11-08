from dataclasses import dataclass
from pysh.core import chars, errors
from pysh.core.regex import regex


@dataclass(kw_only=True, repr=False)
class Error(errors.Error):
    state: state.State
    regex: regex.Regex
