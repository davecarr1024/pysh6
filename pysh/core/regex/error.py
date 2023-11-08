from dataclasses import dataclass
from pysh.core import errors
from pysh.core.regex import regex, state


@dataclass(kw_only=True, repr=False)
class Error(errors.NaryError):
    state: state.State
    regex: regex.Regex
