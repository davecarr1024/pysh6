from dataclasses import dataclass, field
from pysh.pysh import state
from pysh.pysh.statements import block, statement
from pysh.pysh.vals import args, params, type, val
from pysh.pysh.vals.funcs import abstract_func


@dataclass(frozen=True)
class Func(abstract_func.AbstractFunc):
    _name: str
    return_type: type.Type
    params: "params.Params" = field(default_factory=params.Params)
    body: statement.Statement = field(default_factory=block.Block)

    def __str__(self) -> str:
        return f"def {self.name}{self.params} -> {self.return_type}\n{self.body}"

    @property
    def name(self) -> str:
        return self._name

    def __call__(self, state: state.State, args: args.Args) -> val.Val:
        state = self.params.bind(state, args)
        result = self.body.eval(state).return_value_or_none()
        self._try(
            lambda: self.return_type.assert_can_assign(result.type),
            msg=f"invalid return value {result}",
        )
        return result
