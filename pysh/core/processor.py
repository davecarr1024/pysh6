from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, Iterable, Iterator, Mapping, MutableSequence, Optional, Sequence, Sized, Type, TypeVar, Union, overload

from .errors import Error, NaryError


_State = TypeVar('_State')
_Result = TypeVar('_Result')
_AdapterState = TypeVar('_AdapterState')
_AdapterResult = TypeVar('_AdapterResult')


@dataclass(frozen=True,kw_only=True)
class StateError(Generic[_State], Error):
    state: _State

@dataclass(frozen=True,kw_only=True)
class RuleError(Generic[_State, _Result], Error):
    rule: '_AbstractRule[_State,_Result]'

@dataclass(frozen=True,kw_only=True)
class ProcessorError(
    Generic[_State,_Result],
    StateError[_State],
    RuleError[_State,_Result],
    NaryError,
    ):
    ...

@dataclass(frozen=True)
class Scope(Generic[_State,_Result], Mapping[str,'_AbstractRule[_State,_Result]']):
    _rules: Mapping[str,'_AbstractRule[_State,_Result]'] = field(default_factory=dict[str,'_AbstractRule[_State,_Result]'])

    def __getitem__(self, key: str)->'_AbstractRule[_State,_Result]':
        if key not in self._rules:
            raise Error(msg=f'unknown rule {key}')
        return self._rules[key]
    
    def __len__(self)->int:
        return len(self._rules)
    
    def __iter__(self)->Iterator[str]:
        return iter(self._rules)

@dataclass(frozen=True)
class _AbstractStateAndResult(ABC, Generic[_State,_Result]):
    state: _State

    @abstractmethod
    def no(self)->'StateAndNoResult[_State,_Result]':
        ...

    @abstractmethod
    def single(self)->'_StateAndSingleResult[_State,_Result]':
        ...

    @abstractmethod
    def optional(self)->'_StateAndOptionalResult[_State,_Result]':
        ...

    @abstractmethod
    def multiple(self)->'_StateAndMultipleResult[_State,_Result]':
        ...

@dataclass(frozen=True)
class StateAndNoResult(_AbstractStateAndResult[_State,_Result]):
    def no(self)->'StateAndNoResult[_State,_Result]':
        return self
    
    def single(self)->'_StateAndSingleResult[_State,_Result]':
        raise StateError(state=self.state,msg=f'unable to conver StateAndNoResult to StateAndSingleResult')
    
    def optional(self)->'_StateAndOptionalResult[_State,_Result]':
        return _StateAndOptionalResult[_State,_Result](self.state)
    
    def multiple(self)->'_StateAndMultipleResult[_State,_Result]':
        return _StateAndMultipleResult[_State,_Result](self.state)

@dataclass(frozen=True)
class _StateAndSingleResult(_AbstractStateAndResult[_State,_Result]):
    result: _Result

    def no(self)->StateAndNoResult[_State,_Result]:
        return StateAndNoResult[_State,_Result](self.state)
    
    def single(self)->'_StateAndSingleResult[_State,_Result]':
        return self
    
    def optional(self)->'_StateAndOptionalResult[_State,_Result]':
        return _StateAndOptionalResult[_State,_Result](self.state,self.result)

    def multiple(self)->'_StateAndMultipleResult[_State,_Result]':
        return _StateAndMultipleResult[_State,_Result](self.state,[self.result])


@dataclass(frozen=True)
class _StateAndOptionalResult(_AbstractStateAndResult[_State,_Result]):
    result: Optional[_Result] = None

    def no(self)->StateAndNoResult[_State,_Result]:
        return StateAndNoResult[_State,_Result](self.state)
    
    def single(self)->_StateAndSingleResult[_State,_Result]:
        if self.result is None:
            raise StateError[_State](state=self.state,msg=f'unable to convert empty _StateAndOptionalResult to _StateAndSingleResult')
        return _StateAndSingleResult[_State,_Result](self.state,self.result)
    
    def optional(self)->'_StateAndOptionalResult[_State,_Result]':
        return self

    def multiple(self)->'_StateAndMultipleResult[_State,_Result]':
        if self.result:
            return _StateAndMultipleResult[_State,_Result](self.state,[self.result])
        else:
            return _StateAndMultipleResult[_State,_Result](self.state)

@dataclass(frozen=True)
class _StateAndMultipleResult(_AbstractStateAndResult[_State,_Result]):
    results: Sequence[_Result] = field(default_factory=list[_Result])

    def no(self)->StateAndNoResult[_State,_Result]:
        return StateAndNoResult[_State,_Result](self.state)
    
    def single(self)->_StateAndSingleResult[_State,_Result]:
        if len(self.results) != 1:
            raise Error(msg=f'unable to convert {self} to _StateAndSingleResult')
        return _StateAndSingleResult[_State,_Result](self.state,self.results[0])
    
    def optional(self)->_StateAndOptionalResult[_State,_Result]:
        if len(self.results) > 1:
            raise Error(msg=f'unable to convert {self} to _StateAndOptionalResult')
        if self.results:
            return _StateAndOptionalResult[_State,_Result](self.state,self.results[0])
        else:
            return _StateAndOptionalResult[_State,_Result](self.state)

    def multiple(self)->'_StateAndMultipleResult[_State,_Result]':
        return self

_AndArgs = Union[
    'NoResultRule[_State,_Result]',
    'SingleResultRule[_State,_Result]',
    'OptionalResultRule[_State,_Result]',
    'MultipleResultRule[_State,_Result]',
]

class _AbstractRule(ABC, Generic[_State,_Result]):
    @abstractmethod
    def __call__(self, state: _State, scope: Scope[_State,_Result])->_AbstractStateAndResult[_State,_Result]:
        ...

    @abstractmethod
    def no(self)->'NoResultRule[_State,_Result]':
        ...

    @abstractmethod
    def single(self)->'SingleResultRule[_State,_Result]':
        ...

    @abstractmethod
    def optional(self)->'OptionalResultRule[_State,_Result]':
        ...

    @abstractmethod
    def multiple(self)->'MultipleResultRule[_State,_Result]':
        ...

    @overload
    @abstractmethod
    def __and__(self, rhs: 'NoResultRule[_State,_Result]')->'_AbstractAnd[_State,_Result,_AbstractRule[_State,_Result]]':
        ...

    @overload
    @abstractmethod
    def __and__(self, rhs: 'SingleResultRule[_State,_Result]')->'_AbstractAnd[_State,_Result,_AbstractRule[_State,_Result]]':
        ...

    @overload
    @abstractmethod
    def __and__(self, rhs: 'OptionalResultRule[_State,_Result]')->'_AbstractAnd[_State,_Result,_AbstractRule[_State,_Result]]':
        ...

    @overload
    @abstractmethod
    def __and__(self, rhs: 'MultipleResultRule[_State,_Result]')->'_AbstractAnd[_State,_Result,_AbstractRule[_State,_Result]]':
        ...

    @abstractmethod
    def __and__(self, rhs: _AndArgs)->'_AbstractAnd[_State,_Result,_AbstractRule[_State,_Result]]':
        ...

_ChildRuleType = TypeVar('_ChildRuleType',bound=_AbstractRule,covariant=True)

@dataclass(frozen=True)
class _UnaryRule(Generic[_ChildRuleType]):
    child: _ChildRuleType

class NoResultRule(_AbstractRule[_State,_Result]):
    @abstractmethod
    def __call__(self, state: _State, scope: Scope[_State,_Result])->'StateAndNoResult[_State,_Result]':
        ...

    @overload
    def __and__(self, rhs: 'NoResultRule[_State,_Result]')->'_NoResultAnd[_State,_Result]':
        ...

    @overload
    def __and__(self, rhs: 'SingleResultRule[_State,_Result]')->'_SingleResultAnd[_State,_Result]':
        ...

    @overload
    def __and__(self, rhs: 'OptionalResultRule[_State,_Result]')->'_OptionalResultAnd[_State,_Result]':
        ...

    @overload
    def __and__(self, rhs: 'MultipleResultRule[_State,_Result]')->'_MultipleResultAnd[_State,_Result]':
        ...

    def __and__(self, rhs: _AndArgs)->'_AbstractAnd[_State,_Result,_AbstractRule[_State,_Result]]':
        if isinstance(rhs, NoResultRule):
            return _NoResultAnd[_State,_Result]([self,rhs])
        elif isinstance(rhs, SingleResultRule):
            return _SingleResultAnd[_State,_Result]([self,rhs])
        elif isinstance(rhs, OptionalResultRule):
            return _OptionalResultAnd[_State,_Result]([self,rhs])
        elif isinstance(rhs, MultipleResultRule):
            return _MultipleResultAnd[_State,_Result]([self,rhs])
        else:
            raise TypeError(type(rhs))

    def no(self)->'NoResultRule[_State,_Result]':
        return self
    
    def single(self)->'SingleResultRule[_State,_Result]':
        raise RuleError[_State,_Result](rule=self, msg=f'unable to convert NoResultRule to SingleResultRule')
    
    def optional(self)->'OptionalResultRule[_State,_Result]':
        class _Adapter(
            OptionalResultRule[_AdapterState,_AdapterResult],
            _UnaryRule[NoResultRule[_AdapterState,_AdapterResult]],
        ):
            def __call__(self, state: _AdapterState, scope: Scope[_AdapterState,_AdapterResult])->_StateAndOptionalResult[_AdapterState,_AdapterResult]:
                return self.child(state,scope).optional()
        return _Adapter[_State,_Result](self)
    
    def multiple(self)->'MultipleResultRule[_State,_Result]':
        class _Adapter(
            MultipleResultRule[_AdapterState,_AdapterResult],
            _UnaryRule[NoResultRule[_AdapterState,_AdapterResult]],
        ):
            def __call__(self, state: _AdapterState, scope: Scope[_AdapterState,_AdapterResult])->_StateAndMultipleResult[_AdapterState,_AdapterResult]:
                return self.child(state,scope).multiple()
        return _Adapter[_State,_Result](self)
    
class SingleResultRule(_AbstractRule[_State,_Result]):
    @abstractmethod
    def __call__(self, state: _State, scope: Scope[_State,_Result])->_StateAndSingleResult[_State,_Result]:
        ...

    @overload
    def __and__(self, rhs: 'NoResultRule[_State,_Result]')->'_SingleResultAnd[_State,_Result]':
        ...

    @overload
    def __and__(self, rhs: 'SingleResultRule[_State,_Result]')->'_MultipleResultAnd[_State,_Result]':
        ...

    @overload
    def __and__(self, rhs: 'OptionalResultRule[_State,_Result]')->'_MultipleResultAnd[_State,_Result]':
        ...

    @overload
    def __and__(self, rhs: 'MultipleResultRule[_State,_Result]')->'_MultipleResultAnd[_State,_Result]':
        ...

    def __and__(self, rhs: _AndArgs)->'_AbstractAnd[_State,_Result,_AbstractRule[_State,_Result]]':
        if isinstance(rhs, NoResultRule):
            return _SingleResultAnd[_State,_Result]([self,rhs])
        elif isinstance(rhs, SingleResultRule):
            return _MultipleResultAnd[_State,_Result]([self,rhs])
        elif isinstance(rhs, OptionalResultRule):
            return _MultipleResultAnd[_State,_Result]([self,rhs])
        elif isinstance(rhs, MultipleResultRule):
            return _MultipleResultAnd[_State,_Result]([self,rhs])
        else:
            raise TypeError(type(rhs))

    def no(self)->NoResultRule[_State,_Result]:
        class _Adapter(
            NoResultRule[_AdapterState,_AdapterResult],
            _UnaryRule[SingleResultRule[_AdapterState,_AdapterResult]],
            ):
            def __call__(self, state: _AdapterState, scope: Scope[_AdapterState,_AdapterResult])->StateAndNoResult[_AdapterState,_AdapterResult]:
                return self.child(state,scope).no()
        return _Adapter[_State,_Result](self)

    def single(self)->'SingleResultRule[_State,_Result]':
        return self
    
    def optional(self)->'OptionalResultRule[_State,_Result]':
        class _Adapter(
            OptionalResultRule[_AdapterState,_AdapterResult],
            _UnaryRule[SingleResultRule[_AdapterState,_AdapterResult]],
            ):
            def __call__(self, state: _AdapterState, scope: Scope[_AdapterState,_AdapterResult])->_StateAndOptionalResult[_AdapterState,_AdapterResult]:
                return self.child(state,scope).optional()
        return _Adapter[_State,_Result](self)

    def multiple(self)->'MultipleResultRule[_State,_Result]':
        class _Adapter(
            MultipleResultRule[_AdapterState,_AdapterResult],
            _UnaryRule[SingleResultRule[_AdapterState,_AdapterResult]],
        ):
            def __call__(self, state: _AdapterState, scope: Scope[_AdapterState,_AdapterResult])->_StateAndMultipleResult[_AdapterState,_AdapterResult]:
                return self.child(state,scope).multiple()
        return _Adapter[_State,_Result](self)
    

class OptionalResultRule(_AbstractRule[_State,_Result]):
    @abstractmethod
    def __call__(self, state: _State, scope: Scope[_State,_Result])->_StateAndOptionalResult[_State,_Result]:
        ...

    @overload
    def __and__(self, rhs: 'NoResultRule[_State,_Result]')->'_OptionalResultAnd[_State,_Result]':
        ...

    @overload
    def __and__(self, rhs: 'SingleResultRule[_State,_Result]')->'_MultipleResultAnd[_State,_Result]':
        ...

    @overload
    def __and__(self, rhs: 'OptionalResultRule[_State,_Result]')->'_OptionalResultAnd[_State,_Result]':
        ...

    @overload
    def __and__(self, rhs: 'MultipleResultRule[_State,_Result]')->'_MultipleResultAnd[_State,_Result]':
        ...

    def __and__(self, rhs: _AndArgs)->'_AbstractAnd[_State,_Result,_AbstractRule[_State,_Result]]':
        if isinstance(rhs, NoResultRule):
            return _OptionalResultAnd[_State,_Result]([self,rhs])
        elif isinstance(rhs, SingleResultRule):
            return _MultipleResultAnd[_State,_Result]([self,rhs])
        elif isinstance(rhs, OptionalResultRule):
            return _MultipleResultAnd[_State,_Result]([self,rhs])
        elif isinstance(rhs, MultipleResultRule):
            return _MultipleResultAnd[_State,_Result]([self,rhs])
        else:
            raise TypeError(type(rhs))

    def no(self)->NoResultRule[_State,_Result]:
        class _Adapter(
            NoResultRule[_AdapterState,_AdapterResult],
            _UnaryRule[OptionalResultRule[_AdapterState,_AdapterResult]],
            ):
            def __call__(self, state: _AdapterState, scope: Scope[_AdapterState,_AdapterResult])->StateAndNoResult[_AdapterState,_AdapterResult]:
                return self.child(state,scope).no()
        return _Adapter[_State,_Result](self)
    
    def single(self)->SingleResultRule[_State,_Result]:
        class _Adapter(
            SingleResultRule[_AdapterState,_AdapterResult],
            _UnaryRule[OptionalResultRule[_AdapterState,_AdapterResult]],
            ):
            def __call__(self, state: _AdapterState, scope: Scope[_AdapterState,_AdapterResult])->_StateAndSingleResult[_AdapterState,_AdapterResult]:
                return self.child(state,scope).single()
        return _Adapter[_State,_Result](self)

    def optional(self)->'OptionalResultRule[_State,_Result]':
        return self

    def multiple(self)->'MultipleResultRule[_State,_Result]':
        class _Adapter(
            MultipleResultRule[_AdapterState,_AdapterResult],
            _UnaryRule[OptionalResultRule[_AdapterState,_AdapterResult]],
        ):
            def __call__(self, state: _AdapterState, scope: Scope[_AdapterState,_AdapterResult])->_StateAndMultipleResult[_AdapterState,_AdapterResult]:
                return self.child(state,scope).multiple()
        return _Adapter[_State,_Result](self)

class MultipleResultRule(_AbstractRule[_State,_Result]):
    @abstractmethod
    def __call__(self, state: _State, scope: Scope[_State,_Result])->_StateAndMultipleResult[_State,_Result]:
        ...

    @overload
    def __and__(self, rhs: 'NoResultRule[_State,_Result]')->'_MultipleResultAnd[_State,_Result]':
        ...

    @overload
    def __and__(self, rhs: 'SingleResultRule[_State,_Result]')->'_MultipleResultAnd[_State,_Result]':
        ...

    @overload
    def __and__(self, rhs: 'OptionalResultRule[_State,_Result]')->'_OptionalResultAnd[_State,_Result]':
        ...

    @overload
    def __and__(self, rhs: 'MultipleResultRule[_State,_Result]')->'_MultipleResultAnd[_State,_Result]':
        ...

    def __and__(self, rhs: _AndArgs)->'_AbstractAnd[_State,_Result,_AbstractRule[_State,_Result]]':
        if isinstance(rhs, NoResultRule):
            return _MultipleResultAnd[_State,_Result]([self,rhs])
        elif isinstance(rhs, SingleResultRule):
            return _MultipleResultAnd[_State,_Result]([self,rhs])
        elif isinstance(rhs, OptionalResultRule):
            return _MultipleResultAnd[_State,_Result]([self,rhs])
        elif isinstance(rhs, MultipleResultRule):
            return _MultipleResultAnd[_State,_Result]([self,rhs])
        else:
            raise TypeError(type(rhs))


    def no(self)->NoResultRule[_State,_Result]:
        class _Adapter(
            NoResultRule[_AdapterState,_AdapterResult],
            _UnaryRule[MultipleResultRule[_AdapterState,_AdapterResult]],
            ):
            def __call__(self, state: _AdapterState, scope: Scope[_AdapterState,_AdapterResult])->StateAndNoResult[_AdapterState,_AdapterResult]:
                return self.child(state,scope).no()
        return _Adapter[_State,_Result](self)
    
    def single(self)->SingleResultRule[_State,_Result]:
        class _Adapter(
            SingleResultRule[_AdapterState,_AdapterResult],
            _UnaryRule[MultipleResultRule[_AdapterState,_AdapterResult]],
            ):
            def __call__(self, state: _AdapterState, scope: Scope[_AdapterState,_AdapterResult])->_StateAndSingleResult[_AdapterState,_AdapterResult]:
                return self.child(state,scope).single()
        return _Adapter[_State,_Result](self)

    def optional(self)->OptionalResultRule[_State,_Result]:
        class _Adapter(
            OptionalResultRule[_AdapterState,_AdapterResult],
            _UnaryRule[MultipleResultRule[_AdapterState,_AdapterResult]],
            ):
            def __call__(self, state: _AdapterState, scope: Scope[_AdapterState,_AdapterResult])->_StateAndOptionalResult[_AdapterState,_AdapterResult]:
                return self.child(state,scope).optional()
        return _Adapter[_State,_Result](self)

    def multiple(self) -> 'MultipleResultRule[_State, _Result]':
        return self

@dataclass(frozen=True)
class _NaryRule(
    Generic[_State,_Result,_ChildRuleType],
    _AbstractRule[_State,_Result],
    Sized,
    Iterable[_ChildRuleType],
    ):
    _rules: Sequence[_ChildRuleType] = field(default_factory=list[_ChildRuleType])

    def __iter__(self)->Iterator[_ChildRuleType]:
        return iter(self._rules)
    
    def __len__(self)->int:
        return len(self._rules)
    
    def _num_children_of_type(self, type: Type)->int:
        num: int = 0
        for rule in self:
            if isinstance(rule, type):
                num += 1
        return num

    def _assert_num_children_of_type(self, type: Type, expected: int):
        actual = self._num_children_of_type(type)
        if actual != expected:
            raise RuleError(rule=self,msg=f'num children of type {type} {actual} != expected {expected}')

@dataclass(frozen=True)
class _AbstractAnd(_NaryRule[_State,_Result,_ChildRuleType]):
    ...


@dataclass(frozen=True)
class _NoResultAnd(NoResultRule[_State,_Result],_AbstractAnd[_State,_Result,NoResultRule[_State,_Result]]):
    def __call__(self, state: _State, scope: Scope[_State,_Result])->StateAndNoResult[_State,_Result]:
        for rule in self:
            state = rule(state,scope).state
        return StateAndNoResult[_State,_Result](state)

@dataclass(frozen=True)
class _SingleResultAnd(
    SingleResultRule[_State,_Result],
    _AbstractAnd[_State,_Result,NoResultRule[_State,_Result]|SingleResultRule[_State,_Result]],
    ):
    def __post_init__(self):
        self._assert_num_children_of_type(SingleResultRule[_State,_Result],1)

    def __call__(self, state: _State, scope: Scope[_State,_Result])->_StateAndSingleResult[_State,_Result]:
        result: Optional[_Result] = None
        for rule in self:
            state_and_result: _AbstractStateAndResult[_State,_Result] = rule(state,scope)
            state = state_and_result.state
            new_result = state_and_result.optional().result
            if new_result is not None:
                if result is not None:
                    raise ProcessorError[_State,_Result](state=state,rule=self, msg=f'more than one result for SingleResultAnd')
                else:
                    result = new_result
        if result is None:
            raise ProcessorError[_State,_Result](state=state,rule=self, msg=f'no result for SingleResultAnd')
        return _StateAndSingleResult[_State,_Result](state,result)

@dataclass(frozen=True)
class _OptionalResultAnd(
    OptionalResultRule[_State,_Result],
    _AbstractAnd[_State,_Result,NoResultRule[_State,_Result]|OptionalResultRule[_State,_Result]],
    ):
    def __post_init__(self):
        self._assert_num_children_of_type(OptionalResultRule[_State,_Result],1)

    def __call__(self, state: _State, scope: Scope[_State,_Result])->_StateAndOptionalResult[_State,_Result]:
        result: Optional[_Result] = None
        for rule in self:
            state_and_result: _AbstractStateAndResult[_State,_Result] = rule(state,scope)
            state = state_and_result.state
            new_result = state_and_result.optional().result
            if new_result is not None:
                if result is not None:
                    raise ProcessorError[_State,_Result](state=state,rule=self, msg=f'more than one result for OptionalResultAnd')
                else:
                    result = new_result
        return _StateAndOptionalResult[_State,_Result](state,result)

@dataclass(frozen=True)
class _MultipleResultAnd(
    MultipleResultRule[_State,_Result],
    _AbstractAnd[_State,_Result,_AbstractRule[_State,_Result]],
    ):
    def __call__(self, state: _State, scope: Scope[_State,_Result])->_StateAndMultipleResult[_State,_Result]:
        results: MutableSequence[_Result] = []
        for rule in self:
            state_and_result: _AbstractStateAndResult[_State,_Result] = rule(state,scope)
            state = state_and_result.state
            results += state_and_result.multiple().results
        return _StateAndMultipleResult[_State,_Result](state,results)
