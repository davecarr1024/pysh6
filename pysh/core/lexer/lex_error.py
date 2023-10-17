from dataclasses import dataclass
from pysh.core import chars, errors


@dataclass(kw_only=True)
class LexError(errors.NaryError):
    lexer_: "lexer.Lexer"
    state: chars.Stream

    def _repr_line(self) -> str:
        return f"LexError(lexer={self.lexer_},state={self.state},msg={self.msg})"


from pysh.core.lexer import lexer
