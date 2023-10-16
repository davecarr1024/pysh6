from dataclasses import dataclass
from .. import errors


@dataclass(kw_only=True)
class Error(errors.Error):
    ...
