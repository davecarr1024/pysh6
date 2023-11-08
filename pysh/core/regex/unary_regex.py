from dataclasses import dataclass
from pysh.core.regex import regex, state, state_and_result


@dataclass(frozen=True)
class UnaryRegex(regex.Regex):
    child: regex.Regex

    def __call__(self, state: state.State) -> state_and_result.StateAndResult:
        return self.child(state)
