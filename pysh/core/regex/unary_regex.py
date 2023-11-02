from dataclasses import dataclass
from pysh.core import chars
from pysh.core.regex import regex, state_and_result


@dataclass(frozen=True)
class UnaryRegex(regex.Regex):
    child: regex.Regex

    def __call__(self, state: chars.Stream) -> state_and_result.StateAndResult:
        return self.child(state)
