from abc import ABC
from typing import Generic

from pysh.core.parser.state_and_result import result


class Rule(ABC, Generic[result.Result]):
    ...
