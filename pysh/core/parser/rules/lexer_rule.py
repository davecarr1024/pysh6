from dataclasses import dataclass
from typing import TypeVar
from pysh.core import tokens
from pysh.core.parser import states
from pysh.core.parser.rules import state_extractor_rule


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_StateAndResults = TypeVar("_StateAndResults", bound=states.StateAndResults)


@dataclass(frozen=True)
class LexerRule(
    state_extractor_rule.StateExtractorRule[
        _State, _Result, _StateAndResults, tokens.Stream
    ]
):
    ...
