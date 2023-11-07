from dataclasses import dataclass
from typing import Generic, TypeVar
from pysh.core import errors
from pysh.core.parser import results, states
from pysh.core.parser.rules import rule

_State = TypeVar("_State")
_Result = TypeVar("_Result")


@dataclass(kw_only=True)
class Error(Generic[_State, _Result], errors.NaryError):
    rule: rule.Rule[_State, _Result]
    state: _State
