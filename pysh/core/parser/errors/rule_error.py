from dataclasses import dataclass
from pysh.core.parser.errors import error


@dataclass(kw_only=True, repr=False)
class RuleError(error.Error):
    rule: "rule.Rule"

    def _repr_line(self) -> str:
        return f"RuleError({self.rule},msg={self.msg})"


from pysh.core.parser.rules import rule
