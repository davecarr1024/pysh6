from dataclasses import dataclass
from pysh.core import errors


@dataclass(kw_only=True)
class Error(errors.Error):
    ...
