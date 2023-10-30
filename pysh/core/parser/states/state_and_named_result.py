from dataclasses import dataclass
from pysh.core.parser import results

from pysh.core.parser.states import state_and_result


@dataclass(frozen=True)
class StateAndNamedResult(state_and_result.StateAndResult[results.Result]):
    results: results.NamedResult[results.Result]
