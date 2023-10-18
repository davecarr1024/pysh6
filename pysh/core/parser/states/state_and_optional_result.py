from dataclasses import dataclass
from pysh.core.parser import results, states

from pysh.core.parser.states import state_and_result


@dataclass(frozen=True)
class StateAndOptionalResult(state_and_result.StateAndResult[results.Result]):
    results: results.OptionalResult[results.Result]
