from dataclasses import dataclass
from pysh.core.processor import results, states

from pysh.core.processor.states import state_and_result


@dataclass(frozen=True)
class StateAndSingleResult(
    state_and_result.StateAndResult[states.State, results.Result]
):
    results: results.SingleResult[results.Result]
