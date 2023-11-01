from dataclasses import dataclass
from pysh.core.parser import results as results_lib
from pysh.core.parser.states import state_and_result


@dataclass(frozen=True)
class StateAndNamedResult(state_and_result.StateAndResult[results_lib.Result]):
    results: results_lib.NamedResult[results_lib.Result]

    def convert(
        self, func: results_lib.NamedResultConverterFunc[results_lib.ConverterResult]
    ) -> "state_and_single_result.StateAndSingleResult[results_lib.ConverterResult]":
        return state_and_single_result.StateAndSingleResult[
            results_lib.ConverterResult
        ](
            self.state,
            self.results.convert(func),
        )


from pysh.core.parser.states import state_and_single_result
