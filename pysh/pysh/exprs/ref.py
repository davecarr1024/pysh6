from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Self, Sequence
from pysh import core
from pysh.pysh import lexer, parser, vals

from pysh.pysh.exprs import expr


@dataclass(frozen=True)
class Ref(expr.Expr):
    @dataclass(frozen=True)
    class _Head(ABC, core.errors.Errorable["Ref._Head"]):
        @abstractmethod
        def get(self, scope: vals.Scope) -> vals.Val:
            ...

        @abstractmethod
        def set(self, scope: vals.Scope, val: vals.Val) -> None:
            ...

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref._Head"]:
            return Ref._Name.parser_rule() | Ref._Literal.parser_rule()

        @staticmethod
        def create(val: str | vals.Val) -> "Ref._Head":
            match val:
                case str():
                    return Ref._Name(val)
                case vals.Val():
                    return Ref._Literal(val)

    @dataclass(frozen=True)
    class _Name(_Head):
        name: str

        def __str__(self) -> str:
            return self.name

        def get(self, scope: vals.Scope) -> vals.Val:
            return self._try(lambda: scope[self.name].val)

        def set(self, scope: vals.Scope, val: vals.Val) -> None:
            try:
                scope[self.name].val = val
            except core.errors.Error as error:
                raise self._error(children=[error])

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref._Name"]:
            return lexer.id.convert(Ref._Name)

    @dataclass(frozen=True)
    class _Literal(_Head):
        val: vals.Val

        def __str__(self) -> str:
            return str(self.val)

        def get(self, scope: vals.Scope) -> vals.Val:
            return self.val

        def set(self, scope: vals.Scope, val: vals.Val) -> None:
            raise self._error(msg="can't set literal")

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref._Literal"]:
            return vals.Val.parser_rule().convert(Ref._Literal)

    @dataclass(frozen=True)
    class _Tail(ABC, core.errors.Errorable["Ref._Tail"]):
        @abstractmethod
        def get(self, scope: vals.Scope, obj: vals.Val) -> vals.Val:
            ...

        @abstractmethod
        def set(self, scope: vals.Scope, obj: vals.Val, val: vals.Val) -> None:
            ...

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref._Tail"]:
            return Ref._Member.parser_rule() | Ref._Call.parser_rule()

        @staticmethod
        def create(val: str | vals.Args) -> "Ref._Tail":
            match val:
                case str():
                    return Ref._Member(val)
                case vals.Args():
                    return Ref._Call(val)

    @dataclass(frozen=True)
    class _Member(_Tail):
        name: str

        def __str__(self) -> str:
            return f".{self.name}"

        def get(self, scope: vals.Scope, obj: vals.Val) -> vals.Val:
            return self._try(lambda: obj[self.name].val)

        def set(self, scope: vals.Scope, obj: vals.Val, val: vals.Val) -> None:
            try:
                obj[self.name].val = val
            except core.errors.Error as error:
                raise self._error(children=[error])

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref._Member"]:
            return (r"\." & lexer.id).convert(Ref._Member)

    @dataclass(frozen=True)
    class _Call(_Tail):
        args: vals.Args

        def __str__(self) -> str:
            return str(self.args)

        def get(self, scope: vals.Scope, obj: vals.Val) -> vals.Val:
            return self._try(lambda: obj(scope, self.args))

        def set(self, scope: vals.Scope, obj: vals.Val, val: vals.Val) -> None:
            raise self._error(msg="can't set call")

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref._Call"]:
            return vals.Args.parser_rule().convert(Ref._Call)

    head: _Head
    tails: Sequence[_Tail] = field(default_factory=list)

    def eval(self, scope: vals.Scope) -> vals.Val:
        try:
            obj = self.head.get(scope)
            for tail in self.tails:
                obj = tail.get(scope, obj)
            return obj
        except core.errors.Error as error:
            raise self._error(children=[error])

    def set(self, scope: vals.Scope, val: vals.Val) -> None:
        try:
            if len(self.tails) == 0:
                self.head.set(scope, val)
            else:
                obj = self.head.get(scope)
                for tail in self.tails[:-1]:
                    obj = tail.get(scope, obj)
                self.tails[-1].set(scope, obj, val)
        except core.errors.Error as error:
            raise self._error(children=[error])

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref"]:
        return (
            Ref._Head.parser_rule().named("head")
            & Ref._Tail.parser_rule()
            .zero_or_more()
            .convert(lambda tails: tails)
            .named("tails")
        ).convert(Ref)
