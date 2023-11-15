from dataclasses import dataclass, field
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import args, scope, val


@dataclass(frozen=True)
class Object(val.Val):
    class_: "abstract_class.AbstractClass" = field(kw_only=True)

    def __call__(self, scope: scope.Scope, args: args.Args) -> val.Val:
        if "__call__" in self:
            try:
                return self["__call__"](scope, args)
            except core.errors.Error as error:
                raise self._error(children=[error])
        raise self._error(msg="no __call__ method")

    @classmethod
    def parser_rule(
        cls,
    ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Object"]:
        raise NotImplementedError()


from pysh.pype.vals.classes import abstract_class
