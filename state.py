from encodings.punycode import selective_find

from transition import Transition
from datetime import datetime


StateAnnotation = "flowstate.state"
StateId = str


class State:
    def __init__(
        self,
        id: str = "",
        rev: int = 0,
        annotations: dict[str, str] = None,
        labels: dict[str, str] = None,
        commited_at_unix_milli: int = 0,
        transition: "Transition" = None,
    ):
        self.id: str = id
        self.rev: int = rev
        self.annotations: dict[str, str] = annotations
        if self.annotations is None:
            self.annotations = {}

        self.labels: dict[str, str] = labels
        if self.labels is None:
            self.labels = {}

        self.commited_at_unix_milli: int = commited_at_unix_milli
        self.transition: "Transition" = transition
        if self.transition is None:
            self.transition = Transition()

    def set_commited_at(self, commited_at: datetime):
        self.commited_at_unix_milli = round(commited_at.now().timestamp() * 1000)

    def commited_at(self) -> datetime:
        return datetime.fromtimestamp(self.commited_at_unix_milli / 1000)

    def copy_to(self, to: "State") -> "State":
        to.id = self.id
        to.rev = self.rev
        to.annotations = self.annotations.copy()
        to.labels = self.labels.copy()
        to.commited_at_unix_milli = self.commited_at_unix_milli
        self.transition.copy_to(to.transition)

        return to

    def copy_to_ctx(self, to: "StateCtx") -> "StateCtx":
        self.copy_to(to.commited)
        self.copy_to(to.current)
        return to

    def set_annotation(self, name: str, value: str):
        self.annotations[name] = value

    def set_label(self, name: str, value: str):
        self.labels[name] = value


class StateCtx:
    def __init__(
        self,
        current: "State" = None,
        commited: "State" = None,
        transitions: list["Transition"] = None,
        e: "Engine" = None,
    ) -> None:
        self.current: "State" = current
        if self.current is None:
            self.current = State()

        self.commited: "State" = commited
        if self.commited is None:
            self.commited = State()

        self.transitions: list["Transition"] = transitions
        if self.transitions is None:
            self.transitions = []

        self.e: "Engine" = e

    def copy_to(self, to: "StateCtx") -> "StateCtx":
        self.current.copy_to(to.current)
        self.commited.copy_to(to.commited)

        to.transitions = [Transition() for _ in self.transitions]
        for idx in range(len(self.transitions)):
            self.transitions[idx].copy_to(to.transitions[idx])

        return to

    def new_to(self, id: str, to: "StateCtx") -> "StateCtx":
        self.copy_to(to)
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
