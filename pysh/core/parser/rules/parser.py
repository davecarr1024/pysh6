from dataclasses import dataclass
from typing import Optional
from pysh.core import errors, lexer
from pysh.core.parser import results, states
from pysh.core.parser.errors import parse_error
from pysh.core.parser.rules import scope as scope_lib, single_result_rule


@dataclass(frozen=True)
class Parser(single_result_rule.SingleResultRule[results.Result]):
    scope: scope_lib.Scope[results.Result]
    root_rule_name: str

    def __str__(self) -> str:
        return f"Parser(root={repr(self.root_rule_name)}, rules={repr({name: str(rule) for name, rule in self.scope.items()})})"

    def __call__(
        self,
        state: states.State | str,
        scope: Optional[scope_lib.Scope[results.Result]] = None,
        *,
        rule_name: Optional[str] = None,
    ) -> states.StateAndSingleResult[results.Result]:
        if isinstance(state, str):
            state = states.State(self.lexer()(state))
        if scope is None:
            scope = self.scope
        if rule_name is None:
            rule_name = self.root_rule_name
        try:
            return self.scope[rule_name](state, scope)
        except errors.Error as error:
            raise parse_error.ParseError(rule=self, state=state, _children=[error])

    def lexer(self) -> lexer.Lexer:
        lexer_ = lexer.Lexer()
        for rule in self.scope.values():
            lexer_ |= rule.lexer()
        return lexer_
