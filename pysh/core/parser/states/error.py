from dataclasses import dataclass
from pysh.core import errors
from pysh.core.parser.states import state_and_results


@dataclass(kw_only=True)
class Error(errors.Error):
    state_and_results: "state_and_results.StateAndResults"
