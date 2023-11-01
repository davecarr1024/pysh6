from dataclasses import dataclass
from pysh.core.parser import results
from pysh.core.parser.rules import child_rule, nary_rule


@dataclass(frozen=True)
class Or(nary_rule.NaryRule[results.Result, child_rule.ChildRule]):
    ...
