from dataclasses import dataclass
from pysh import core
from pysh.pype import parser
from pysh.pype.vals import scope
from pysh.pype.funcs import abstract_func, bindable_func, func
from pysh.pype.statements import result, statement


@dataclass(frozen=True)
class Func(statement.Statement):
    func: abstract_func.AbstractFunc

    def eval(self, scope: scope.Scope) -> result.Result:
        scope[self.func.name()] = self.func
        return result.Result()

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Func"]:
        return func.Func.parser_rule().convert(Func)

    def as_bindable(self) -> "Func":
        return Func(bindable_func.BindableFunc(func=self.func))
