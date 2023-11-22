from .expr import Expr
from .ref import Ref

from pysh.pysh.vals import val as _val
from pysh.pysh.vals import builtins as _builtins


def literal(val: _val.Val) -> Ref:
    return Ref.create(val)


def ref_(val: str) -> Ref:
    return Ref.create(val)
