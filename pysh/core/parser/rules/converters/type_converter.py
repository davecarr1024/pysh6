from dataclasses import dataclass, field
from typing import Generic
from pysh.core.parser import results
from pysh.core.parser.rules import (
    child_rule,
    rule,
    scope as scope_lib,
    single_result_rule,
)
from pysh.core.parser.rules.unary_rules import unary_rule


@dataclass(frozen=True)
class TypeConverter(
    Generic[results.Result, results.ConverterResult, child_rule.ChildRule],
    single_result_rule.SingleResultRule[results.ConverterResult],
    unary_rule.UnaryRule[results.ConverterResult, rule.Rule[results.Result]],
):
    ...
