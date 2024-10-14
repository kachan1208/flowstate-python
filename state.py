from engine import Engine
from transition import Transition
from datetime import datetime


StateAnnotation = "flowstate.state"
StateId = str


class State:
    def __init__(self) -> None:
        self.id: str = ""
        self.rev: int = 0
        self.annotations: dict[str, str]
        self.labels: dict[str, str]
        self.commitedAtUnixMilli: int = 0
        self.transition: Transition = Transition()

    def setCommitedAt(self, commitedAt: datetime):
        self.commitedAtUnixMilli = round(commitedAt.now().timestamp() * 1000)

    def commitedAt(self) -> datetime:
        return datetime.fromtimestamp(self.commitedAtUnixMilli / 1000)

    def copyTo(self, to: "State") -> "State":
        to.id = self.id
        to.rev = self.rev
        to.annotations = self.annotations.copy()
        to.labels = self.labels.copy()
        to.commitedAtUnixMilli = self.commitedAtUnixMilli
        self.transition.CopyTo(to.transition)

        return to

    def copyToCtx(self, to: "StateCtx") -> "StateCtx":
        self.copyTo(to.commited)
        self.copyTo(to.current)
        return to

    def setAnnotation(self, name: str, value: str):
        self.annotations[name] = value

    def setLabel(self, name: str, value: str):
        self.labels[name] = value


class StateCtx:
    current: State
    commited: State
    transitions: list[Transition]
    e: Engine

    def __init__(
        self, current: State, commited: State, transitions: list[Transition], e: Engine
    ) -> None:
        self.current = current
        self.commited = commited
        self.transitions = transitions
        self.e = e

    def copyTo(self, to: "StateCtx") -> "StateCtx":
        self.current.copyTo(to.current)
        self.commited.copyTo(to.commited)

        if len(to.transitions) >= len(self.transitions):
            to.transitions = to.transitions[: len(self.transitions)]
        else:
            to.transitions = [Transition() for _ in range(len(self.transitions))]

        for idx in range(len(self.transitions)):
            self.transitions[idx].copyTo(to.transitions[idx])

        return to

    def newTo(self, id: str, to: "StateCtx") -> "StateCtx":
        self.copyTo(to)
        to.current.id = id
        to.current.rev = 0
        to.current.id = id
        to.current.rev = 0
        return to

    def deadline(self) -> tuple[datetime, bool]:
        return datetime.now(), False

    # TODO: implement me
    def done(self) -> bool:
        return False

    # TODO: implement me
    def err(self) -> Exception:
        return Exception("Not implemented")

    def value(self, key: str) -> any:
        return self.current.annotations[key]

    def __copy__(self):
        return None

    def __deepcopy__(self):
        return None
