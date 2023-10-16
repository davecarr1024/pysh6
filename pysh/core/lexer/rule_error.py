from dataclasses import dataclass
from .. import chars, errors


@dataclass
class RuleError(errors.UnaryError):
    rule: "rule.Rule"
    state: chars.Stream

    def _repr_line(self) -> str:
        return f"RuleError(rule={self.rule},state={self.state},msg={self.msg})"


from . import rule
