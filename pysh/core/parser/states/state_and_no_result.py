from dataclasses import dataclass
from pysh.core.parser import results as results_lib

from pysh.core.parser.states import state_and_result


@dataclass(frozen=True)
class StateAndNoResult(state_and_result.StateAndResult[results_lib.Result]):
    results: results_lib.NoResult[results_lib.Result]

    def convert_type(
        self, func: results_lib.NoResultConverterFunc[results_lib.ConverterResult]
    ) -> "state_and_single_result.StateAndSingleResult[results_lib.ConverterResult]":
        return state_and_single_result.StateAndSingleResult[
            results_lib.ConverterResult
        ](self.state, self.results.convert_type(func))


from pysh.core.parser.states import state_and_single_result
