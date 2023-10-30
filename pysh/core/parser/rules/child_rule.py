from typing import TypeVar

from pysh.core.parser.rules import rule


ChildRule = TypeVar("ChildRule", bound=rule.Rule, covariant=True)
