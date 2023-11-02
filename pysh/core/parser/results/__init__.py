from pysh.core.parser.results.error import Error
from pysh.core.parser.results.result import Result
from pysh.core.parser.results.converter_result import ConverterResult
from pysh.core.parser.results.results import Results
from pysh.core.parser.results.no_result import NoResult, NoResultConverterFunc
from pysh.core.parser.results.single_result import (
    SingleResult,
    SingleResultConverterFunc,
)
from pysh.core.parser.results.optional_result import (
    OptionalResult,
    OptionalResultConverterFunc,
)
from pysh.core.parser.results.multiple_result import (
    MultipleResult,
    MultipleResultConverterFunc,
)
from pysh.core.parser.results.named_result import (
    NamedResult,
    NamedResultConverterFunc,
)
from pysh.core.parser.results.or_args import OrArgs
