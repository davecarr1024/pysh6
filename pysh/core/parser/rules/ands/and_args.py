from typing import Union
from pysh.core.parser import results

from pysh.core.parser.rules import (
    multiple_results_rule,
    named_results_rule,
    no_result_rule,
    optional_result_rule,
    single_result_rule,
)


AndArgs = Union[
    no_result_rule.NoResultRule[results.Result],
    single_result_rule.SingleResultRule[results.Result],
    optional_result_rule.OptionalResultRule[results.Result],
    multiple_results_rule.MultipleResultsRule[results.Result],
    named_results_rule.NamedResultsRule[results.Result],
]
