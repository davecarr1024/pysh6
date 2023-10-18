from dataclasses import dataclass
from typing import Generic, Type
from pysh.core.parser import errors
from pysh.core.parser.results import result, results


@dataclass(kw_only=True)
class Error(errors.Error, Generic[result.Result]):
    result: "result.Result | results.Results | Type[results.Results]"
