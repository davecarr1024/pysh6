from pysh import core


id_lexer_rule = core.lexer.Rule.load(
    "id",
    core.regex.NotIn(
        core.regex.Regex.load(r"([a-z]|[A-Z])+"),
        [
            "def",
            "lambda",
        ],
    ),
)
