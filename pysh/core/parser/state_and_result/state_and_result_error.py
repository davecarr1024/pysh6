from dataclasses import dataclass
from typing import Generic

from pysh.core.parser import errors
from pysh.core.parser.state_and_result import abstract_state_and_result, result


@dataclass(kw_only=True)
class StateAndResultError(errors.Error, Generic[result.Result]):
    state_and_result: abstract_state_and_result.AbstractStateAndResult[result.Result]
