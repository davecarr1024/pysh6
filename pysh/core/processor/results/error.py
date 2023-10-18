from dataclasses import dataclass
from typing import Generic, Type
from pysh.core.processor import errors
from pysh.core.processor.results import result, results


@dataclass(kw_only=True)
class Error(errors.Error, Generic[result.Result]):
    result: "result.Result | results.Results | Type[results.Results]"
