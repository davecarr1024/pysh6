from pysh.pype.vals.scope import Scope
from pysh.pype.vals.val import Val
from pysh.pype.vals.arg import Arg
from pysh.pype.vals.args import Args
from pysh.pype.vals import builtins, classes

none = builtins.none


def int_(value: int) -> builtins.Int:
    return builtins.Int.create(value)
