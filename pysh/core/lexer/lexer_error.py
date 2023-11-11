from dataclasses import dataclass
from pysh.core import errors
from pysh.core.lexer import state


@dataclass(kw_only=True, repr=False)
class LexerError(errors.NaryError):
    lexer: "lexer.Lexer"
    state: state.State

    def _repr_line(self) -> str:
        return f"LexerError(lexer={self.lexer},state={self.state},msg={self.msg})"


from pysh.core.lexer import lexer
