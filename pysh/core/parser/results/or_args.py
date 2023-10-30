from typing import Union
from pysh.core.parser.results import (
    result,
    no_result,
    single_result,
    optional_result,
    multiple_result,
    named_result,
)


OrArgs = Union[
    no_result.NoResult[result.Result],
    single_result.SingleResult[result.Result],
    optional_result.OptionalResult[result.Result],
    multiple_result.MultipleResult[result.Result],
    named_result.NamedResult[result.Result],
]
