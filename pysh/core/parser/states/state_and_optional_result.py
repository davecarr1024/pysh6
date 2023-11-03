from dataclasses import dataclass
from pysh.core.parser import results as results_lib
from pysh.core.parser.states import state_and_result


@dataclass(frozen=True)
class StateAndOptionalResult(state_and_result.StateAndResult[results_lib.Result]):
    results: results_lib.OptionalResult[results_lib.Result]

    def convert_type(
        self,
        func: results_lib.OptionalResultConverterFunc[
            results_lib.Result, results_lib.ConverterResult
        ],
    ) -> "state_and_single_result.StateAndSingleResult[results_lib.ConverterResult]":
        return state_and_single_result.StateAndSingleResult[
            results_lib.ConverterResult
        ](
            self.state,
            self.results.convert_type(func),
        )

    def convert(
        self,
        func: results_lib.OptionalResultConverterFunc[
            results_lib.Result, results_lib.Result
        ],
    ) -> "state_and_single_result.StateAndSingleResult[results_lib.Result]":
        return state_and_single_result.StateAndSingleResult[results_lib.Result](
            self.state, self.results.convert(func)
        )


from pysh.core.parser.states import state_and_single_result
