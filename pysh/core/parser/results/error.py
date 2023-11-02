from dataclasses import dataclass
from typing import Type
from pysh.core.parser import errors
from pysh.core.parser.results import result, results


@dataclass(kw_only=True, repr=False)
class Error(errors.Error):
    result: "results.Results | Type[results.Results]"

    def _repr_line(self) -> str:
        return f"Error({self.result})"
