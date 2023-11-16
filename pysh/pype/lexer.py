from pysh import core


id = core.lexer.Rule.load("id", r"([a-z]|[A-Z]|_)([a-z]|[A-Z]|_|\d)*")
