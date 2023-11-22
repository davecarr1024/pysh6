from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Sequence
from pysh import core
from pysh.pysh import lexer, parser, state
from pysh.pysh.vals import args, scope, val
from pysh.pysh.exprs import expr


@dataclass(frozen=True)
class Ref(expr.Expr):
    @dataclass(frozen=True)
    class _Head(ABC, core.errors.Errorable["Ref._Head"]):
        @abstractmethod
        def get(self, scope: scope.Scope) -> val.Val:
            ...

        @abstractmethod
        def set(self, scope: scope.Scope, val: val.Val) -> None:
            ...

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref._Head"]:
            return Ref._Name.parser_rule() | Ref._Literal.parser_rule()

        @staticmethod
        def create(val_: str | val.Val) -> "Ref._Head":
            match val_:
                case str():
                    return Ref._Name(val_)
                case val.Val():
                    return Ref._Literal(val_)

    @dataclass(frozen=True)
    class _Name(_Head):
        name: str

        def __str__(self) -> str:
            return self.name

        def get(self, scope: scope.Scope) -> val.Val:
            return self._try(lambda: scope[self.name].val)

        def set(self, scope: scope.Scope, val: val.Val) -> None:
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
        val_: val.Val

        def __str__(self) -> str:
            return str(self.val_)

        def get(self, scope: scope.Scope) -> "val.Val":
            return self.val_

        def set(self, scope: scope.Scope, val: "val.Val") -> None:
            raise self._error(msg="can't set literal")

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref._Literal"]:
            return val.Val.parser_rule().convert(Ref._Literal)

    @dataclass(frozen=True)
    class _Tail(ABC, core.errors.Errorable["Ref._Tail"]):
        @abstractmethod
        def get(self, scope: scope.Scope, obj: val.Val) -> val.Val:
            ...

        @abstractmethod
        def set(self, scope: scope.Scope, obj: val.Val, val: val.Val) -> None:
            ...

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref._Tail"]:
            return Ref._Member.parser_rule() | Ref._Call.parser_rule()

        @staticmethod
        def create(val: str | args.Args) -> "Ref._Tail":
            match val:
                case str():
                    return Ref._Member(val)
                case args.Args():
                    return Ref._Call(val)

    @dataclass(frozen=True)
    class _Member(_Tail):
        name: str

        def __str__(self) -> str:
            return f".{self.name}"

        def get(self, scope: scope.Scope, obj: val.Val) -> val.Val:
            return self._try(lambda: obj[self.name].val)

        def set(self, scope: scope.Scope, obj: val.Val, val: val.Val) -> None:
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
        args: args.Args

        def __str__(self) -> str:
            return str(self.args)

        def get(self, scope: scope.Scope, obj: val.Val) -> val.Val:
            return self._try(lambda: obj(scope, self.args))

        def set(self, scope: scope.Scope, obj: val.Val, val: val.Val) -> None:
            raise self._error(msg="can't set call")

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref._Call"]:
            return args.Args.parser_rule().convert(Ref._Call)

    head: _Head
    tails: Sequence[_Tail] = field(default_factory=list)

    def eval(self, state: state.State) -> val.Val:
        try:
            obj = self.head.get(state.scope)
            for tail in self.tails:
                obj = tail.get(state.scope, obj)
            return obj
        except core.errors.Error as error:
            raise self._error(children=[error])

    def set(self, scope: scope.Scope, val: val.Val) -> None:
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
