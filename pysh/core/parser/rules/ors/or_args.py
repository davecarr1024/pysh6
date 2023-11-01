from typing import Union
from pysh.core.parser import results

from pysh.core.parser.rules import (
    no_result_rule,
    single_result_rule,
    optional_result_rule,
    multiple_result_rule,
    named_result_rule,
)


OrArgs = Union[
    no_result_rule.NoResultRule[results.Result],
    single_result_rule.SingleResultRule[results.Result],
    optional_result_rule.OptionalResultRule[results.Result],
    multiple_result_rule.MultipleResultRule[results.Result],
    named_result_rule.NamedResultRule[results.Result],
]
