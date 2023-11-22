from pysh import core
from pysh.pysh import parser


id = core.parser.rules.Literal[parser.Parser](
    core.lexer.Rule.load(
        "id",
        core.regex.NotIn(
            core.regex.Regex.load(
                r"([a-z]|[A-Z]|_)([a-z]|[A-Z]|_|\d)*",
            ),
            [
                "def",
                "return",
            ],
        ),
    )
).token_value()
