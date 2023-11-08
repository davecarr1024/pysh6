from dataclasses import dataclass
from pysh.core import errors, regex, tokens
from pysh.core.lexer import result, rule_error, state, state_and_result


@dataclass(frozen=True)
class Rule:
    name: str
    regex_: regex.Regex

    def __str__(self) -> str:
        if self.name == str(self.regex_):
            return self.name
        else:
            return f"{self.name}={self.regex_}"

    def __call__(self, state_: state.State) -> state_and_result.StateAndResult:
        try:
            regex_state_and_result = self.regex_(regex.State(state_.chars))
            return state_and_result.StateAndResult(
                state.State(regex_state_and_result.state.chars),
                result.Result(
                    tokens.Stream([regex_state_and_result.result.token(self.name)]),
                ),
            )
        except errors.Error as error:
            raise rule_error.RuleError(rule=self, state=state_, child=error)

    @staticmethod
    def load(rule_name: str, regex_: str | regex.Regex | None = None) -> "Rule":
        if regex_ is None:
            regex_ = regex.Regex.load(rule_name)
        if isinstance(regex_, str):
            regex_ = regex.Regex.load(regex_)
        return Rule(rule_name, regex_)
