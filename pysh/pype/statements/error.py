from dataclasses import dataclass
from pysh import core


@dataclass(kw_only=True, repr=False)
class Error(core.errors.NaryError):
    statement: "statement.Statement"

    def _repr_line(self) -> str:
        return f"StatementError({self.statement},{repr(self.msg)})"


from pysh.pype.statements import statement
