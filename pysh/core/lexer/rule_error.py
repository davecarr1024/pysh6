from dataclasses import dataclass
from pysh.core import errors
from pysh.core.lexer import state


@dataclass(
    kw_only=True,
    repr=False,
)
class RuleError(errors.UnaryError):
    rule: "rule.Rule"
    state: "state.State"

    def _repr_line(self) -> str:
        return f"RuleError(rule={self.rule},state={self.state},msg={self.msg})"


from pysh.core.lexer import rule
