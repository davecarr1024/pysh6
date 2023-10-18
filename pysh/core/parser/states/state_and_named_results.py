from dataclasses import dataclass
from pysh.core.parser import results

from pysh.core.parser.states import state_and_result


@dataclass(frozen=True)
class StateAndNamedResults(state_and_result.StateAndResult[results.Result]):
    results: results.NamedResults[results.Result]
