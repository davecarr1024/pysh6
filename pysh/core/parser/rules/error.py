from dataclasses import dataclass
from typing import Generic, TypeVar
from pysh.core import errors

_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(kw_only=True)
class Error(
    errors.NaryError,
    Generic[_State, _Result],
):
    rule: "rule.Rule[_State, _Result]"
    state: _State


from pysh.core.parser.rules import rule
