from dataclasses import dataclass
from pysh.core.parser import results

from pysh.core.parser.states import state_and_result


@dataclass(frozen=True)
class StateAndNoResult(state_and_result.StateAndResult[results.Result]):
    results: results.NoResult[results.Result]
