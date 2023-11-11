from dataclasses import dataclass
from pysh.core import errors
from pysh.core.parser.results import results


@dataclass(kw_only=True, repr=False)
class Error(errors.Error):
    results: results.Results
