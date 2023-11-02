from dataclasses import dataclass
from pysh.core import chars, errors, regex
from pysh.core.lexer import rule_error, state_and_result


@dataclass(frozen=True)
class Rule:
    name: str
    regex_: regex.Regex

    def __str__(self) -> str:
        if self.name == str(self.regex_):
            return repr(self.name)
        else:
            return f"{self.name}={repr(str(self.regex_))}"

    def __call__(self, state: str | chars.Stream) -> state_and_result.StateAndResult:
        if isinstance(state, str):
            state = chars.Stream.load(state)
        try:
            state, result = self.regex_(state)
            return state, result.token(self.name)
        except errors.Error as error:
            raise rule_error.RuleError(rule=self, state=state, child=error)

    @staticmethod
    def load(rule_name: str, regex_: str | regex.Regex | None = None) -> "Rule":
        if regex_ is None:
            regex_ = regex.Regex.load(rule_name)
        if isinstance(regex_, str):
            regex_ = regex.Regex.load(regex_)
        return Rule(rule_name, regex_)
