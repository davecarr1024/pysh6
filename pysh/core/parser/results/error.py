from dataclasses import dataclass
from typing import Generic
from pysh.core.parser import errors
from pysh.core.parser.results import result


@dataclass(kw_only=True)
class Error(errors.Error, Generic[result.Result]):
    result: "result.Result"
