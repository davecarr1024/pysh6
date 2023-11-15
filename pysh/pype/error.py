from dataclasses import dataclass

from pysh import core


@dataclass(kw_only=True, repr=False)
class Error(core.errors.Error):
    ...
