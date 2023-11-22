from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Sequence
from pysh import core
from pysh.pysh import lexer, parser, state
from pysh.pysh.vals import args, val, var
from pysh.pysh.exprs import expr


@dataclass(frozen=True)
class Ref(expr.Expr):
    @dataclass(frozen=True)
    class Head(ABC, core.errors.Errorable["Ref.Head"]):
        @abstractmethod
        def get(self, state: state.State) -> val.Val:
            ...

        @abstractmethod
        def set(self, state: state.State, val: val.Val) -> None:
            ...

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref.Head"]:
            return Ref.Name.parser_rule() | Ref.Literal.parser_rule()

        def _error_name(self) -> str:
            return f"Ref.Head.{self.__class__.__name__}.Error"

        @staticmethod
        def create(val_: str | val.Val) -> "Ref.Head":
            match val_:
                case str():
                    return Ref.Name(val_)
                case val.Val():
                    return Ref.Literal(val_)

    @dataclass(frozen=True)
    class Name(Head):
        name: str

        def __str__(self) -> str:
            return self.name

        def get(self, state: state.State) -> val.Val:
            return self._try(lambda: state[self.name].val)

        def set(self, state: state.State, val: val.Val) -> None:
            try:
                state[self.name].val = val
            except core.errors.Error as error:
                raise self._error(children=[error])

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref.Name"]:
            return lexer.id.convert(Ref.Name)

    @dataclass(frozen=True)
    class Literal(Head):
        val_: val.Val

        def __str__(self) -> str:
            return str(self.val_)

        def get(self, state: state.State) -> "val.Val":
            return self.val_

        def set(self, state: state.State, val: "val.Val") -> None:
            raise self._error(msg="can't set literal")

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref.Literal"]:
            return val.Val.parser_rule().convert(Ref.Literal)

    @dataclass(frozen=True)
    class Tail(ABC, core.errors.Errorable["Ref.Tail"]):
        @abstractmethod
        def get(self, state: state.State, obj: val.Val) -> val.Val:
            ...

        @abstractmethod
        def set(self, state: state.State, obj: val.Val, val: val.Val) -> None:
            ...

        def _error_name(self) -> str:
            return f"Ref.Tail.{self.__class__.__name__}.Error"

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref.Tail"]:
            return Ref.Member.parser_rule() | Ref.Call.parser_rule()

        @staticmethod
        def create(val: str | args.Args) -> "Ref.Tail":
            match val:
                case str():
                    return Ref.Member(val)
                case args.Args():
                    return Ref.Call(val)

    @dataclass(frozen=True)
    class Member(Tail):
        name: str

        def __str__(self) -> str:
            return f".{self.name}"

        def get(self, state: state.State, obj: val.Val) -> val.Val:
            return self._try(lambda: obj[self.name].val)

        def set(self, state: state.State, obj: val.Val, val: val.Val) -> None:
            try:
                obj[self.name].val = val
            except core.errors.Error as error:
                raise self._error(children=[error])

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref.Member"]:
            return (r"\." & lexer.id).convert(Ref.Member)

    @dataclass(frozen=True)
    class Call(Tail):
        args: args.Args

        def __str__(self) -> str:
            return str(self.args)

        def get(self, state: state.State, obj: val.Val) -> val.Val:
            return self._try(lambda: obj(state, self.args))

        def set(self, state: state.State, obj: val.Val, val: val.Val) -> None:
            raise self._error(msg="can't set call")

        @classmethod
        def parser_rule(
            cls,
        ) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref.Call"]:
            return args.Args.parser_rule().convert(Ref.Call)

    head: Head
    tails: Sequence[Tail] = field(default_factory=list)

    def __str__(self) -> str:
        return f'{self.head}{"".join(map(str,self.tails))}'

    def eval(self, state: state.State) -> val.Val:
        try:
            obj = self.head.get(state)
            for tail in self.tails:
                obj = tail.get(state, obj)
            return obj
        except core.errors.Error as error:
            raise self._error(
                children=[error],
                msg="get",
            )

    def set(self, state: state.State, val: val.Val) -> None:
        try:
            if len(self.tails) == 0:
                self.head.set(state, val)
            else:
                obj = self.head.get(state)
                for tail in self.tails[:-1]:
                    obj = tail.get(state, obj)
                self.tails[-1].set(state, obj, val)
        except core.errors.Error as error:
            raise self._error(
                children=[error],
                msg=f"set = {val}",
            )

    @staticmethod
    def create(head: str | val.Val, *tails: str | args.Args) -> "Ref":
        return Ref(Ref.Head.create(head), list(map(Ref.Tail.create, tails)))

    @classmethod
    def parser_rule(cls) -> core.parser.rules.SingleResultsRule[parser.Parser, "Ref"]:
        return (
            Ref.Head.parser_rule().named("head")
            & Ref.Tail.parser_rule()
            .zero_or_more()
            .convert(lambda tails: tails)
            .named("tails")
        ).convert(Ref)
