from dataclasses import dataclass
from typing import Type
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import classes


@dataclass(
    frozen=True,
    kw_only=True,
)
class Class(classes.AbstractClass):
    _name: str
    _object_type: Type["object_.Object"]

    def create(self, *args, **kwargs) -> "object_.Object":
        return self._object_type(
            class_=self,
            members=self.members.as_child(),
            *args,
            **kwargs,
        )

    def name(self) -> str:
        return self._name

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Class"]:
        raise NotImplementedError()


from pysh.pype.vals.builtins import object_
