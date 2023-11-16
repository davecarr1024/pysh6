from pysh import core


id = core.lexer.Rule.load(
    "id",
    core.regex.NotIn(
        core.regex.Regex.load(r"([a-z]|[A-Z]|_)([a-z]|[A-Z]|_|\d)*"),
        [
            "class",
        ],
    ),
)
