from dataclasses import dataclass
from pysh.core import errors
from pysh.core.parser import states
from pysh.core.parser.errors import error


@dataclass(kw_only=True, repr=False)
class ParseError(
    errors.NaryError,
    error.Error,
):
    rule: "rules.Rule"
    state: states.State

    def _repr_line(self) -> str:
        return f"ParseError(rule={self.rule},state={self.state},msg={self.msg})"


from pysh.core.parser import rules
