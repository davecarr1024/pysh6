from dataclasses import dataclass
from pysh.core import errors


@dataclass(kw_only=True, repr=False)
class Error(errors.Error):
    ...
