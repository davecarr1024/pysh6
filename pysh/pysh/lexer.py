from pysh import core
from pysh.pysh import parser


id = core.parser.rules.Literal[parser.Parser](
    core.lexer.Rule.load(
        "id",
        r"([a-z]|[A-Z]|_)([a-z]|[A-Z]|_|\d)*",
    )
).token_value()
