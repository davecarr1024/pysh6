from abc import abstractmethod
from dataclasses import dataclass, field
from pysh.pype.vals import classes, scope


@dataclass(frozen=True, kw_only=True)
class Object(classes.Object):
    class_: "class_.Class" = field(
        compare=False,
        hash=False,
        repr=False,
    )
    members: scope.Scope = field(
        compare=False,
        hash=False,
        repr=False,
    )


from pysh.pype.vals.builtins import class_
