from dataclasses import dataclass
from pysh.core import errors
from pysh.core.parser import results
from pysh.core.parser.errors import rule_error, state_error


@dataclass(kw_only=True)
class ParseError(
    state_error.StateError,
    rule_error.RuleError[results.Result],
    errors.NaryError["ParseError[results.Result]"],
):
    ...
