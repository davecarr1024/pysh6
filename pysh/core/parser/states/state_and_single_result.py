from dataclasses import dataclass
from pysh.core.parser import results as results_lib
from pysh.core.parser.states import state_and_result


@dataclass(frozen=True)
class StateAndSingleResult(state_and_result.StateAndResult[results_lib.Result]):
    results: results_lib.SingleResult[results_lib.Result]

    def convert(
        self,
        func: results_lib.SingleResultConverterFunc[
            results_lib.Result, results_lib.ConverterResult
        ],
    ) -> "StateAndSingleResult[results_lib.ConverterResult]":
        return StateAndSingleResult[results_lib.ConverterResult](
            self.state, self.results.convert(func)
        )
