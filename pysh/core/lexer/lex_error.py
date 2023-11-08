from dataclasses import dataclass
from pysh.core import errors
from pysh.core.lexer import state


@dataclass(kw_only=True, repr=False)
class LexError(errors.NaryError):
    lexer_: "lexer.Lexer"
    state: state.State

    def _repr_line(self) -> str:
        return f"LexError(lexer={self.lexer_},state={self.state},msg={self.msg})"


from pysh.core.lexer import lexer
