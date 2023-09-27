from dataclasses import dataclass
from typing import Optional
from . import errors, processor, stream, stream_test

import unittest

_State = stream_test.IntStream
_Result = int
_Scope = processor.Scope[_State,_Result]
_StateAndNoResult = processor._StateAndNoResult[_State,_Result]

@dataclass(frozen=True)
class _Eq(processor.NoResultRule[_State,_Result]):
    val: int

    def __call__(self, state: _State, scope: _Scope)->_StateAndNoResult:
        if state.head() != self.val:
            raise errors.Error(msg=f'head {state.head()} != expected {self.val}')
        return _StateAndNoResult(state.tail())

class EqTest(unittest.TestCase):
    def test_call(self):
        for state, rule, expected in list[tuple[_State,_Eq,Optional[_State]]]([
            (
                _State(),
                _Eq(1),
                None,
            ),
            (
                _State([2]),
                _Eq(1),
                None,
            ),
            (
                _State([1]),
                _Eq(1),
                _State(),
            ),
            (
                _State([1,2]),
                _Eq(1),
                _State([2]),
            ),
        ]):
            with self.subTest(state=state,rule=rule,expected=expected):
                if expected is None:
                    with self.assertRaises(errors.Error):
                        rule(state,_Scope())
                else:
                    self.assertEqual(rule(state,_Scope()).state,expected)