from dataclasses import dataclass, field


@dataclass(frozen=True)
class State:
    scope: "scope.Scope" = field(default_factory=lambda: scope.Scope())

    def __str__(self) -> str:
        return str(self.scope)


from .vals import scope
