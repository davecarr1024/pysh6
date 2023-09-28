from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Sized,
    Type,
    TypeVar,
    Union,
    overload,
)

from .errors import Error, NaryError


_State = TypeVar("_State")
_Result = TypeVar("_Result")
_AdapterState = TypeVar("_AdapterState")
_AdapterResult = TypeVar("_AdapterResult")
_ConverterResult = TypeVar("_ConverterResult")
_AdapterConverterResult = TypeVar("_AdapterConverterResult")


@dataclass(frozen=True, kw_only=True)
class StateError(Generic[_State], Error):
    state: _State


@dataclass(frozen=True, kw_only=True)
class RuleError(Generic[_State, _Result], Error):
    rule: "Rule[_State,_Result]"


@dataclass(frozen=True, kw_only=True)
class ProcessorError(
    Generic[_State, _Result],
    StateError[_State],
    RuleError[_State, _Result],
    NaryError,
):
    ...


@dataclass(frozen=True)
class Scope(Generic[_State, _Result], Mapping[str, "Rule[_State,_Result]"]):
    _rules: Mapping[str, "Rule[_State,_Result]"] = field(
        default_factory=dict[str, "Rule[_State,_Result]"]
    )

    def __getitem__(self, key: str) -> "Rule[_State,_Result]":
        if key not in self._rules:
            raise Error(msg=f"unknown rule {key}")
        return self._rules[key]

    def __len__(self) -> int:
        return len(self._rules)

    def __iter__(self) -> Iterator[str]:
        return iter(self._rules)


class Converter(ABC, Generic[_State, _Result, _ConverterResult]):
    @abstractmethod
    def __call__(self, result: _Result) -> _ConverterResult:
        ...

    @abstractmethod
    def scope(self) -> Scope[_State, _Result]:
        ...


@dataclass(frozen=True)
class _AbstractStateAndResult(ABC, Generic[_State, _Result]):
    state: _State

    @abstractmethod
    def no(self) -> "_StateAndNoResult[_State,_Result]":
        ...

    @abstractmethod
    def single(self) -> "_StateAndSingleResult[_State,_Result]":
        ...

    @abstractmethod
    def optional(self) -> "_StateAndOptionalResult[_State,_Result]":
        ...

    @abstractmethod
    def multiple(self) -> "_StateAndMultipleResults[_State,_Result]":
        ...

    @abstractmethod
    def named(self) -> "_StateAndNamedResults[_State,_Result]":
        ...

    @abstractmethod
    def convert(
        self, converter: Converter[_State, _Result, _ConverterResult]
    ) -> "_AbstractStateAndResult[_State,_ConverterResult]":
        ...


@dataclass(frozen=True)
class _StateAndNoResult(_AbstractStateAndResult[_State, _Result]):
    def no(self) -> "_StateAndNoResult[_State,_Result]":
        return self

    def single(self) -> "_StateAndSingleResult[_State,_Result]":
        raise StateError(
            state=self.state,
            msg=f"unable to conver StateAndNoResult to StateAndSingleResult",
        )

    def optional(self) -> "_StateAndOptionalResult[_State,_Result]":
        return _StateAndOptionalResult[_State, _Result](self.state)

    def multiple(self) -> "_StateAndMultipleResults[_State,_Result]":
        return _StateAndMultipleResults[_State, _Result](self.state)

    def named(self) -> "_StateAndNamedResults[_State,_Result]":
        return _StateAndNamedResults[_State, _Result](self.state)

    def convert(
        self, converter: Converter[_State, _Result, _ConverterResult]
    ) -> "_StateAndNoResult[_State,_ConverterResult]":
        return _StateAndNoResult[_State, _ConverterResult](self.state)


@dataclass(frozen=True)
class _StateAndSingleResult(_AbstractStateAndResult[_State, _Result]):
    result: _Result

    def no(self) -> _StateAndNoResult[_State, _Result]:
        return _StateAndNoResult[_State, _Result](self.state)

    def single(self) -> "_StateAndSingleResult[_State,_Result]":
        return self

    def optional(self) -> "_StateAndOptionalResult[_State,_Result]":
        return _StateAndOptionalResult[_State, _Result](self.state, self.result)

    def multiple(self) -> "_StateAndMultipleResults[_State,_Result]":
        return _StateAndMultipleResults[_State, _Result](self.state, [self.result])

    def named(self) -> "_StateAndNamedResults[_State,_Result]":
        return _StateAndNamedResults[_State, _Result](
            self.state, [_NamedResult(value=self.result)]
        )

    def convert(
        self, converter: Converter[_State, _Result, _ConverterResult]
    ) -> "_StateAndSingleResult[_State,_ConverterResult]":
        return _StateAndSingleResult[_State, _ConverterResult](
            self.state, converter(self.result)
        )


@dataclass(frozen=True)
class _StateAndOptionalResult(_AbstractStateAndResult[_State, _Result]):
    result: Optional[_Result] = None

    def no(self) -> _StateAndNoResult[_State, _Result]:
        return _StateAndNoResult[_State, _Result](self.state)

    def single(self) -> _StateAndSingleResult[_State, _Result]:
        if self.result is None:
            raise StateError[_State](
                state=self.state,
                msg=f"unable to convert empty _StateAndOptionalResult to _StateAndSingleResult",
            )
        return _StateAndSingleResult[_State, _Result](self.state, self.result)

    def optional(self) -> "_StateAndOptionalResult[_State,_Result]":
        return self

    def multiple(self) -> "_StateAndMultipleResults[_State,_Result]":
        if self.result:
            return _StateAndMultipleResults[_State, _Result](self.state, [self.result])
        else:
            return _StateAndMultipleResults[_State, _Result](self.state)

    def named(self) -> "_StateAndNamedResults[_State, _Result]":
        if self.result:
            return _StateAndNamedResults[_State, _Result](
                self.state, [_NamedResult(value=self.result)]
            )
        else:
            return _StateAndNamedResults[_State, _Result](self.state)

    def convert(
        self, converter: Converter[_State, _Result, _ConverterResult]
    ) -> "_StateAndOptionalResult[_State,_ConverterResult]":
        if self.result is None:
            return _StateAndOptionalResult[_State, _ConverterResult](self.state)
        else:
            return _StateAndOptionalResult[_State, _ConverterResult](
                self.state, converter(self.result)
            )


@dataclass(frozen=True)
class _StateAndMultipleResults(_AbstractStateAndResult[_State, _Result]):
    results: Sequence[_Result] = field(default_factory=list[_Result])

    def no(self) -> _StateAndNoResult[_State, _Result]:
        return _StateAndNoResult[_State, _Result](self.state)

    def single(self) -> _StateAndSingleResult[_State, _Result]:
        if len(self.results) != 1:
            raise Error(msg=f"unable to convert {self} to _StateAndSingleResult")
        return _StateAndSingleResult[_State, _Result](self.state, self.results[0])

    def optional(self) -> _StateAndOptionalResult[_State, _Result]:
        if len(self.results) > 1:
            raise Error(msg=f"unable to convert {self} to _StateAndOptionalResult")
        if self.results:
            return _StateAndOptionalResult[_State, _Result](self.state, self.results[0])
        else:
            return _StateAndOptionalResult[_State, _Result](self.state)

    def multiple(self) -> "_StateAndMultipleResults[_State,_Result]":
        return self

    def named(self) -> "_StateAndNamedResults[_State,_Result]":
        return _StateAndNamedResults[_State, _Result](
            self.state, [_NamedResult(value=result) for result in self.results]
        )

    def convert(
        self, converter: Converter[_State, _Result, _ConverterResult]
    ) -> "_StateAndMultipleResults[_State,_ConverterResult]":
        return _StateAndMultipleResults[_State, _ConverterResult](
            self.state, [converter(result) for result in self.results]
        )


@dataclass(frozen=True, kw_only=True)
class _NamedResult(Generic[_Result]):
    name: Optional[str] = None
    value: _Result

    def convert(
        self, converter: Converter[Any, _Result, _ConverterResult]
    ) -> "_NamedResult[_ConverterResult]":
        return _NamedResult[_ConverterResult](
            name=self.name, value=converter(self.value)
        )


@dataclass(frozen=True)
class _StateAndNamedResults(_AbstractStateAndResult[_State, _Result]):
    results: Sequence[_NamedResult[_Result]] = field(
        default_factory=list[_NamedResult[_Result]]
    )

    def __getitem__(self, name: str) -> _Result:
        for result in self.results:
            if result.name and result.name == name:
                return result.value
        raise Error(msg=f"unknown named result {name}")

    def no(self) -> _StateAndNoResult[_State, _Result]:
        return _StateAndNoResult[_State, _Result](self.state)

    def single(self) -> _StateAndSingleResult[_State, _Result]:
        raise Error(msg=f"unable to convert {self} to _StateAndSingleResult")

    def optional(self) -> _StateAndOptionalResult[_State, _Result]:
        raise Error(msg=f"unable to convert {self} to _StateAndOptionalResult")

    def multiple(self) -> _StateAndMultipleResults[_State, _Result]:
        return _StateAndMultipleResults[_State, _Result](
            self.state, [result.value for result in self.results]
        )

    def named(self) -> "_StateAndNamedResults[_State,_Result]":
        return self

    def convert(
        self, converter: Converter[_State, _Result, _ConverterResult]
    ) -> "_StateAndNamedResults[_State, _ConverterResult]":
        return _StateAndNamedResults[_State, _ConverterResult](
            self.state, [result.convert(converter) for result in self.results]
        )


_AndArgs = Union[
    "NoResultRule[_State,_Result]",
    "SingleResultRule[_State,_Result]",
    "OptionalResultRule[_State,_Result]",
    "MultipleResultsRule[_State,_Result]",
    "NamedResultsRule[_State,_Result]",
]


class Rule(ABC, Generic[_State, _Result]):
    @abstractmethod
    def __call__(
        self, state: _State, scope: Scope[_State, _Result]
    ) -> _AbstractStateAndResult[_State, _Result]:
        ...

    @abstractmethod
    def no(self) -> "NoResultRule[_State,_Result]":
        ...

    @abstractmethod
    def single(self) -> "SingleResultRule[_State,_Result]":
        ...

    @abstractmethod
    def optional(self) -> "OptionalResultRule[_State,_Result]":
        ...

    @abstractmethod
    def multiple(self) -> "MultipleResultsRule[_State,_Result]":
        ...

    @abstractmethod
    def named(self) -> "NamedResultsRule[_State,_Result]":
        ...

    @abstractmethod
    def convert(
        self, converter: Converter[_State, _Result, _AdapterResult]
    ) -> "Rule[_State,_AdapterResult]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "NoResultRule[_State,_Result]"
    ) -> "_AbstractAnd[_State,_Result,Rule[_State,_Result]]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "SingleResultRule[_State,_Result]"
    ) -> "_AbstractAnd[_State,_Result,Rule[_State,_Result]]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "OptionalResultRule[_State,_Result]"
    ) -> "_AbstractAnd[_State,_Result,Rule[_State,_Result]]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "MultipleResultsRule[_State,_Result]"
    ) -> "_AbstractAnd[_State,_Result,Rule[_State,_Result]]":
        ...

    @overload
    @abstractmethod
    def __and__(
        self, rhs: "NamedResultsRule[_State,_Result]"
    ) -> "_AbstractAnd[_State,_Result,Rule[_State,_Result]]":
        ...

    @abstractmethod
    def __and__(
        self, rhs: _AndArgs
    ) -> "_AbstractAnd[_State,_Result,Rule[_State,_Result]]":
        ...


_ChildRuleType = TypeVar("_ChildRuleType", bound=Rule, covariant=True)


@dataclass(frozen=True)
class _UnaryRule(Generic[_ChildRuleType]):
    child: _ChildRuleType


class NoResultRule(Rule[_State, _Result]):
    @abstractmethod
    def __call__(
        self, state: _State, scope: Scope[_State, _Result]
    ) -> "_StateAndNoResult[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "NoResultRule[_State,_Result]"
    ) -> "_NoResultAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "SingleResultRule[_State,_Result]"
    ) -> "_SingleResultAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "OptionalResultRule[_State,_Result]"
    ) -> "_OptionalResultAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "MultipleResultsRule[_State,_Result]"
    ) -> "_MultipleResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "NamedResultsRule[_State,_Result]"
    ) -> "_NamedResultsAnd[_State,_Result]":
        ...

    def __and__(
        self, rhs: _AndArgs
    ) -> "_AbstractAnd[_State,_Result,Rule[_State,_Result]]":
        if isinstance(rhs, NoResultRule):
            return _NoResultAnd[_State, _Result]([self, rhs])
        elif isinstance(rhs, SingleResultRule):
            return _SingleResultAnd[_State, _Result]([self, rhs])
        elif isinstance(rhs, OptionalResultRule):
            return _OptionalResultAnd[_State, _Result]([self, rhs])
        elif isinstance(rhs, MultipleResultsRule):
            return _MultipleResultsAnd[_State, _Result]([self, rhs])
        elif isinstance(rhs, NamedResultsRule):
            return _NamedResultsAnd[_State, _Result]([self, rhs])
        else:
            raise TypeError(type(rhs))

    def no(self) -> "NoResultRule[_State,_Result]":
        return self

    def single(self) -> "SingleResultRule[_State,_Result]":
        raise RuleError[_State, _Result](
            rule=self, msg=f"unable to convert NoResultRule to SingleResultRule"
        )

    def optional(self) -> "OptionalResultRule[_State,_Result]":
        class Adapter(
            OptionalResultRule[_AdapterState, _AdapterResult],
            _UnaryRule[NoResultRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndOptionalResult[_AdapterState, _AdapterResult]:
                return self.child(state, scope).optional()

        return Adapter[_State, _Result](self)

    def multiple(self) -> "MultipleResultsRule[_State,_Result]":
        class Adapter(
            MultipleResultsRule[_AdapterState, _AdapterResult],
            _UnaryRule[NoResultRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndMultipleResults[_AdapterState, _AdapterResult]:
                return self.child(state, scope).multiple()

        return Adapter[_State, _Result](self)

    def named(self) -> "NamedResultsRule[_State,_Result]":
        class Adapter(
            NamedResultsRule[_AdapterState, _AdapterResult],
            _UnaryRule[NoResultRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndNamedResults[_AdapterState, _AdapterResult]:
                return self.child(state, scope).named()

        return Adapter[_State, _Result](self)

    def convert(
        self, converter: Converter[_State, _Result, _ConverterResult]
    ) -> "NoResultRule[_State,_ConverterResult]":
        @dataclass(frozen=True)
        class Adapter(
            Generic[_AdapterState, _AdapterResult, _AdapterConverterResult],
            NoResultRule[_AdapterState, _AdapterConverterResult],
            _UnaryRule[NoResultRule[_AdapterState, _AdapterResult]],
        ):
            converter: Converter[_AdapterState, _AdapterResult, _AdapterConverterResult]

            def __call__(
                self,
                state: _AdapterState,
                scope: Scope[_AdapterState, _AdapterConverterResult],
            ) -> _StateAndNoResult[_AdapterState, _AdapterConverterResult]:
                return self.child(state, self.converter.scope()).convert(self.converter)

        return Adapter[_State, _Result, _ConverterResult](self, converter)


class SingleResultRule(Rule[_State, _Result]):
    @abstractmethod
    def __call__(
        self, state: _State, scope: Scope[_State, _Result]
    ) -> _StateAndSingleResult[_State, _Result]:
        ...

    @overload
    def __and__(
        self, rhs: "NoResultRule[_State,_Result]"
    ) -> "_SingleResultAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "SingleResultRule[_State,_Result]"
    ) -> "_MultipleResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "OptionalResultRule[_State,_Result]"
    ) -> "_MultipleResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "MultipleResultsRule[_State,_Result]"
    ) -> "_MultipleResultsAnd[_State,_Result]":
        ...

    def __and__(
        self, rhs: _AndArgs
    ) -> "_AbstractAnd[_State,_Result,Rule[_State,_Result]]":
        if isinstance(rhs, NoResultRule):
            return _SingleResultAnd[_State, _Result]([self, rhs])
        elif isinstance(rhs, SingleResultRule):
            return _MultipleResultsAnd[_State, _Result]([self, rhs])
        elif isinstance(rhs, OptionalResultRule):
            return _MultipleResultsAnd[_State, _Result]([self, rhs])
        elif isinstance(rhs, MultipleResultsRule):
            return _MultipleResultsAnd[_State, _Result]([self, rhs])
        else:
            raise TypeError(type(rhs))

    def no(self) -> NoResultRule[_State, _Result]:
        class Adapter(
            NoResultRule[_AdapterState, _AdapterResult],
            _UnaryRule[SingleResultRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndNoResult[_AdapterState, _AdapterResult]:
                return self.child(state, scope).no()

        return Adapter[_State, _Result](self)

    def single(self) -> "SingleResultRule[_State,_Result]":
        return self

    def optional(self) -> "OptionalResultRule[_State,_Result]":
        class Adapter(
            OptionalResultRule[_AdapterState, _AdapterResult],
            _UnaryRule[SingleResultRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndOptionalResult[_AdapterState, _AdapterResult]:
                return self.child(state, scope).optional()

        return Adapter[_State, _Result](self)

    def multiple(self) -> "MultipleResultsRule[_State,_Result]":
        class Adapter(
            MultipleResultsRule[_AdapterState, _AdapterResult],
            _UnaryRule[SingleResultRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndMultipleResults[_AdapterState, _AdapterResult]:
                return self.child(state, scope).multiple()

        return Adapter[_State, _Result](self)

    def named(self) -> "NamedResultsRule[_State,_Result]":
        class Adapter(
            NamedResultsRule[_AdapterState, _AdapterResult],
            _UnaryRule[SingleResultRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndNamedResults[_AdapterState, _AdapterResult]:
                return self.child(state, scope).named()

        return Adapter[_State, _Result](self)

    def convert(
        self, converter: Converter[_State, _Result, _ConverterResult]
    ) -> "SingleResultRule[_State,_ConverterResult]":
        @dataclass(frozen=True)
        class Adapter(
            Generic[_AdapterState, _AdapterResult, _AdapterConverterResult],
            SingleResultRule[_AdapterState, _AdapterConverterResult],
            _UnaryRule[SingleResultRule[_AdapterState, _AdapterResult]],
        ):
            converter: Converter[_AdapterState, _AdapterResult, _AdapterConverterResult]

            def __call__(
                self,
                state: _AdapterState,
                scope: Scope[_AdapterState, _AdapterConverterResult],
            ) -> _StateAndSingleResult[_AdapterState, _AdapterConverterResult]:
                return self.child(state, self.converter.scope()).convert(self.converter)

        return Adapter[_State, _Result, _ConverterResult](self, converter)

    def zero_or_one(self) -> "OptionalResultRule[_State,_Result]":
        @dataclass(frozen=True)
        class Adapter(
            OptionalResultRule[_AdapterState, _AdapterResult],
            _UnaryRule[SingleResultRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndOptionalResult[_AdapterState, _AdapterResult]:
                try:
                    return self.child(state, scope).optional()
                except Error:
                    return _StateAndOptionalResult[_AdapterState, _AdapterResult](state)

        return Adapter[_State, _Result](self)

    def zero_or_more(self) -> "MultipleResultsRule[_State,_Result]":
        @dataclass(frozen=True)
        class Adapter(
            MultipleResultsRule[_AdapterState, _AdapterResult],
            _UnaryRule[SingleResultRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndMultipleResults[_AdapterState, _AdapterResult]:
                results: MutableSequence[_AdapterResult] = []
                while True:
                    try:
                        state_and_result = self.child(state, scope)
                    except Error:
                        return _StateAndMultipleResults[_AdapterState, _AdapterResult](
                            state, results
                        )
                    state = state_and_result.state
                    results.append(state_and_result.result)

        return Adapter[_State, _Result](self)

    def one_or_more(self) -> "MultipleResultsRule[_State,_Result]":
        @dataclass(frozen=True)
        class Adapter(
            MultipleResultsRule[_AdapterState, _AdapterResult],
            _UnaryRule[SingleResultRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndMultipleResults[_AdapterState, _AdapterResult]:
                results: MutableSequence[_AdapterResult] = []
                try:
                    state_and_result = self.child(state, scope)
                except Error as error:
                    raise ProcessorError(rule=self, state=state, children=[error])
                while True:
                    try:
                        state_and_result = self.child(state, scope)
                    except Error:
                        return _StateAndMultipleResults[_AdapterState, _AdapterResult](
                            state, results
                        )
                    state = state_and_result.state
                    results.append(state_and_result.result)

        return Adapter[_State, _Result](self)


class OptionalResultRule(Rule[_State, _Result]):
    @abstractmethod
    def __call__(
        self, state: _State, scope: Scope[_State, _Result]
    ) -> _StateAndOptionalResult[_State, _Result]:
        ...

    @overload
    def __and__(
        self, rhs: "NoResultRule[_State,_Result]"
    ) -> "_OptionalResultAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "SingleResultRule[_State,_Result]"
    ) -> "_MultipleResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "OptionalResultRule[_State,_Result]"
    ) -> "_OptionalResultAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "MultipleResultsRule[_State,_Result]"
    ) -> "_MultipleResultsAnd[_State,_Result]":
        ...

    def __and__(
        self, rhs: _AndArgs
    ) -> "_AbstractAnd[_State,_Result,Rule[_State,_Result]]":
        if isinstance(rhs, NoResultRule):
            return _OptionalResultAnd[_State, _Result]([self, rhs])
        elif isinstance(rhs, SingleResultRule):
            return _MultipleResultsAnd[_State, _Result]([self, rhs])
        elif isinstance(rhs, OptionalResultRule):
            return _MultipleResultsAnd[_State, _Result]([self, rhs])
        elif isinstance(rhs, MultipleResultsRule):
            return _MultipleResultsAnd[_State, _Result]([self, rhs])
        else:
            raise TypeError(type(rhs))

    def no(self) -> NoResultRule[_State, _Result]:
        class Adapter(
            NoResultRule[_AdapterState, _AdapterResult],
            _UnaryRule[OptionalResultRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndNoResult[_AdapterState, _AdapterResult]:
                return self.child(state, scope).no()

        return Adapter[_State, _Result](self)

    def single(self) -> SingleResultRule[_State, _Result]:
        class Adapter(
            SingleResultRule[_AdapterState, _AdapterResult],
            _UnaryRule[OptionalResultRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndSingleResult[_AdapterState, _AdapterResult]:
                return self.child(state, scope).single()

        return Adapter[_State, _Result](self)

    def optional(self) -> "OptionalResultRule[_State,_Result]":
        return self

    def multiple(self) -> "MultipleResultsRule[_State,_Result]":
        class Adapter(
            MultipleResultsRule[_AdapterState, _AdapterResult],
            _UnaryRule[OptionalResultRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndMultipleResults[_AdapterState, _AdapterResult]:
                return self.child(state, scope).multiple()

        return Adapter[_State, _Result](self)

    def named(self) -> "NamedResultsRule[_State,_Result]":
        class Adapter(
            NamedResultsRule[_AdapterState, _AdapterResult],
            _UnaryRule[SingleResultRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndNamedResults[_AdapterState, _AdapterResult]:
                return self.child(state, scope).named()

        return Adapter[_State, _Result](self)

    def convert(
        self, converter: Converter[_State, _Result, _ConverterResult]
    ) -> "OptionalResultRule[_State,_ConverterResult]":
        @dataclass(frozen=True)
        class Adapter(
            Generic[_AdapterState, _AdapterResult, _AdapterConverterResult],
            OptionalResultRule[_AdapterState, _AdapterConverterResult],
            _UnaryRule[OptionalResultRule[_AdapterState, _AdapterResult]],
        ):
            converter: Converter[_AdapterState, _AdapterResult, _AdapterConverterResult]

            def __call__(
                self,
                state: _AdapterState,
                scope: Scope[_AdapterState, _AdapterConverterResult],
            ) -> _StateAndOptionalResult[_AdapterState, _AdapterConverterResult]:
                return self.child(state, self.converter.scope()).convert(self.converter)

        return Adapter[_State, _Result, _ConverterResult](self, converter)


class MultipleResultsRule(Rule[_State, _Result]):
    @abstractmethod
    def __call__(
        self, state: _State, scope: Scope[_State, _Result]
    ) -> _StateAndMultipleResults[_State, _Result]:
        ...

    @overload
    def __and__(
        self, rhs: "NoResultRule[_State,_Result]"
    ) -> "_MultipleResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "SingleResultRule[_State,_Result]"
    ) -> "_MultipleResultsAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "OptionalResultRule[_State,_Result]"
    ) -> "_OptionalResultAnd[_State,_Result]":
        ...

    @overload
    def __and__(
        self, rhs: "MultipleResultsRule[_State,_Result]"
    ) -> "_MultipleResultsAnd[_State,_Result]":
        ...

    def __and__(
        self, rhs: _AndArgs
    ) -> "_AbstractAnd[_State,_Result,Rule[_State,_Result]]":
        if isinstance(rhs, NoResultRule):
            return _MultipleResultsAnd[_State, _Result]([self, rhs])
        elif isinstance(rhs, SingleResultRule):
            return _MultipleResultsAnd[_State, _Result]([self, rhs])
        elif isinstance(rhs, OptionalResultRule):
            return _MultipleResultsAnd[_State, _Result]([self, rhs])
        elif isinstance(rhs, MultipleResultsRule):
            return _MultipleResultsAnd[_State, _Result]([self, rhs])
        else:
            raise TypeError(type(rhs))

    def no(self) -> NoResultRule[_State, _Result]:
        class Adapter(
            NoResultRule[_AdapterState, _AdapterResult],
            _UnaryRule[MultipleResultsRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndNoResult[_AdapterState, _AdapterResult]:
                return self.child(state, scope).no()

        return Adapter[_State, _Result](self)

    def single(self) -> SingleResultRule[_State, _Result]:
        class Adapter(
            SingleResultRule[_AdapterState, _AdapterResult],
            _UnaryRule[MultipleResultsRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndSingleResult[_AdapterState, _AdapterResult]:
                return self.child(state, scope).single()

        return Adapter[_State, _Result](self)

    def optional(self) -> OptionalResultRule[_State, _Result]:
        class Adapter(
            OptionalResultRule[_AdapterState, _AdapterResult],
            _UnaryRule[MultipleResultsRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndOptionalResult[_AdapterState, _AdapterResult]:
                return self.child(state, scope).optional()

        return Adapter[_State, _Result](self)

    def multiple(self) -> "MultipleResultsRule[_State, _Result]":
        return self

    def named(self) -> "NamedResultsRule[_State,_Result]":
        class Adapter(
            NamedResultsRule[_AdapterState, _AdapterResult],
            _UnaryRule[MultipleResultsRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndNamedResults[_AdapterState, _AdapterResult]:
                return self.child(state, scope).named()

        return Adapter[_State, _Result](self)

    def convert(
        self, converter: Converter[_State, _Result, _ConverterResult]
    ) -> "MultipleResultsRule[_State,_ConverterResult]":
        @dataclass(frozen=True)
        class Adapter(
            Generic[_AdapterState, _AdapterResult, _AdapterConverterResult],
            MultipleResultsRule[_AdapterState, _AdapterConverterResult],
            _UnaryRule[MultipleResultsRule[_AdapterState, _AdapterResult]],
        ):
            converter: Converter[_AdapterState, _AdapterResult, _AdapterConverterResult]

            def __call__(
                self,
                state: _AdapterState,
                scope: Scope[_AdapterState, _AdapterConverterResult],
            ) -> _StateAndMultipleResults[_AdapterState, _AdapterConverterResult]:
                return self.child(state, self.converter.scope()).convert(self.converter)

        return Adapter[_State, _Result, _ConverterResult](self, converter)


@dataclass(frozen=True)
class NamedResultsRule(Rule[_State, _Result]):
    @abstractmethod
    def __call__(
        self, state: _State, scope: Scope[_State, _Result]
    ) -> _StateAndNamedResults[_State, _Result]:
        ...

    def no(self) -> NoResultRule[_State, _Result]:
        class Adapter(
            NoResultRule[_AdapterState, _AdapterResult],
            _UnaryRule[NamedResultsRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndNoResult[_AdapterState, _AdapterResult]:
                return self.child(state, scope).no()

        return Adapter[_State, _Result](self)

    def single(self) -> SingleResultRule[_State, _Result]:
        class Adapter(
            SingleResultRule[_AdapterState, _AdapterResult],
            _UnaryRule[NamedResultsRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndSingleResult[_AdapterState, _AdapterResult]:
                return self.child(state, scope).single()

        return Adapter[_State, _Result](self)

    def optional(self) -> OptionalResultRule[_State, _Result]:
        class Adapter(
            OptionalResultRule[_AdapterState, _AdapterResult],
            _UnaryRule[NamedResultsRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndOptionalResult[_AdapterState, _AdapterResult]:
                return self.child(state, scope).optional()

        return Adapter[_State, _Result](self)

    def multiple(self) -> MultipleResultsRule[_State, _Result]:
        class Adapter(
            MultipleResultsRule[_AdapterState, _AdapterResult],
            _UnaryRule[NamedResultsRule[_AdapterState, _AdapterResult]],
        ):
            def __call__(
                self, state: _AdapterState, scope: Scope[_AdapterState, _AdapterResult]
            ) -> _StateAndMultipleResults[_AdapterState, _AdapterResult]:
                return self.child(state, scope).multiple()

        return Adapter[_State, _Result](self)

    def named(self) -> "NamedResultsRule[_State,_Result]":
        return self

    def convert(
        self, converter: Converter[_State, _Result, _ConverterResult]
    ) -> "NamedResultsRule[_State,_ConverterResult]":
        @dataclass(frozen=True)
        class Adapter(
            Generic[_AdapterState, _AdapterResult, _AdapterConverterResult],
            NamedResultsRule[_AdapterState, _AdapterConverterResult],
            _UnaryRule[NamedResultsRule[_AdapterState, _AdapterResult]],
        ):
            converter: Converter[_AdapterState, _AdapterResult, _AdapterConverterResult]

            def __call__(
                self,
                state: _AdapterState,
                scope: Scope[_AdapterState, _AdapterConverterResult],
            ) -> _StateAndNamedResults[_AdapterState, _AdapterConverterResult]:
                return self.child(state, self.converter.scope()).convert(self.converter)

        return Adapter[_State, _Result, _ConverterResult](self, converter)


@dataclass(frozen=True)
class _NaryRule(
    Generic[_State, _Result, _ChildRuleType],
    Rule[_State, _Result],
    Sized,
    Iterable[_ChildRuleType],
):
    _rules: Sequence[_ChildRuleType] = field(default_factory=list[_ChildRuleType])

    def __iter__(self) -> Iterator[_ChildRuleType]:
        return iter(self._rules)

    def __len__(self) -> int:
        return len(self._rules)

    def _num_children_of_type(self, type: Type) -> int:
        num: int = 0
        for rule in self:
            if isinstance(rule, type):
                num += 1
        return num

    def _assert_num_children_of_type(self, type: Type, expected: int):
        actual = self._num_children_of_type(type)
        if actual != expected:
            raise RuleError(
                rule=self,
                msg=f"num children of type {type} {actual} != expected {expected}",
            )


@dataclass(frozen=True)
class _AbstractAnd(_NaryRule[_State, _Result, _ChildRuleType]):
    ...


@dataclass(frozen=True)
class _NoResultAnd(
    NoResultRule[_State, _Result],
    _AbstractAnd[_State, _Result, NoResultRule[_State, _Result]],
):
    def __call__(
        self, state: _State, scope: Scope[_State, _Result]
    ) -> _StateAndNoResult[_State, _Result]:
        for rule in self:
            try:
                state = rule(state, scope).state
            except Error as error:
                raise ProcessorError(rule=self, state=state, children=[error])
        return _StateAndNoResult[_State, _Result](state)


@dataclass(frozen=True)
class _SingleResultAnd(
    SingleResultRule[_State, _Result],
    _AbstractAnd[
        _State,
        _Result,
        NoResultRule[_State, _Result] | SingleResultRule[_State, _Result],
    ],
):
    def __post_init__(self):
        self._assert_num_children_of_type(SingleResultRule[_State, _Result], 1)

    def __call__(
        self, state: _State, scope: Scope[_State, _Result]
    ) -> _StateAndSingleResult[_State, _Result]:
        result: Optional[_Result] = None
        for rule in self:
            try:
                state_and_result: _AbstractStateAndResult[_State, _Result] = rule(
                    state, scope
                )
            except Error as error:
                raise ProcessorError(rule=self, state=state, children=[error])
            state = state_and_result.state
            new_result = state_and_result.optional().result
            if new_result is not None:
                if result is not None:
                    raise ProcessorError[_State, _Result](
                        state=state,
                        rule=self,
                        msg=f"more than one result for SingleResultAnd",
                    )
                else:
                    result = new_result
        if result is None:
            raise ProcessorError[_State, _Result](
                state=state, rule=self, msg=f"no result for SingleResultAnd"
            )
        return _StateAndSingleResult[_State, _Result](state, result)


@dataclass(frozen=True)
class _OptionalResultAnd(
    OptionalResultRule[_State, _Result],
    _AbstractAnd[
        _State,
        _Result,
        NoResultRule[_State, _Result] | OptionalResultRule[_State, _Result],
    ],
):
    def __post_init__(self):
        self._assert_num_children_of_type(OptionalResultRule[_State, _Result], 1)

    def __call__(
        self, state: _State, scope: Scope[_State, _Result]
    ) -> _StateAndOptionalResult[_State, _Result]:
        result: Optional[_Result] = None
        for rule in self:
            try:
                state_and_result: _AbstractStateAndResult[_State, _Result] = rule(
                    state, scope
                )
            except Error as error:
                raise ProcessorError(rule=self, state=state, children=[error])
            state = state_and_result.state
            new_result = state_and_result.optional().result
            if new_result is not None:
                if result is not None:
                    raise ProcessorError[_State, _Result](
                        state=state,
                        rule=self,
                        msg=f"more than one result for OptionalResultAnd",
                    )
                else:
                    result = new_result
        return _StateAndOptionalResult[_State, _Result](state, result)


@dataclass(frozen=True)
class _MultipleResultsAnd(
    MultipleResultsRule[_State, _Result],
    _AbstractAnd[_State, _Result, Rule[_State, _Result]],
):
    def __call__(
        self, state: _State, scope: Scope[_State, _Result]
    ) -> _StateAndMultipleResults[_State, _Result]:
        results: MutableSequence[_Result] = []
        for rule in self:
            try:
                state_and_result: _AbstractStateAndResult[_State, _Result] = rule(
                    state, scope
                )
            except Error as error:
                raise ProcessorError(rule=self, state=state, children=[error])
            state = state_and_result.state
            results += state_and_result.multiple().results
        return _StateAndMultipleResults[_State, _Result](state, results)


@dataclass(frozen=True)
class _NamedResultRule(
    NamedResultsRule[_State, _Result],
    _UnaryRule[SingleResultRule[_State, _Result]],
):
    name: Optional[str] = None


@dataclass(frozen=True)
class _NamedResultsAnd(
    NamedResultsRule[_State, _Result],
    _AbstractAnd[
        _State,
        _Result,
        Union[
            _NamedResultRule[_State, _Result],
            NamedResultsRule[_State, _Result],
            NoResultRule[_State, _Result],
        ],
    ],
):
    def __call__(
        self, state: _State, scope: Scope[_State, _Result]
    ) -> _StateAndNamedResults[_State, _Result]:
        results: MutableMapping[str, _Result] = {}
        for rule in self:
            try:
                state_and_result: _AbstractStateAndResult[_State, _Result] = rule(
                    state, scope
                )
            except Error as error:
                raise ProcessorError(rule=self, state=state, children=[error])
            state = state_and_result.state
            results |= {
                result.name: result.value
                for result in state_and_result.named().results
                if result.name is not None
            }
        return _StateAndNamedResults[_State, _Result](
            state,
            [
                _NamedResult[_Result](name=name, value=value)
                for name, value in results.items()
            ],
        )
