from state import StateCtx, StateId
from command import Command


def GetById(stateCtx: StateCtx, id: StateId, rev: int) -> "GetCommand":
    return GetCommand(stateCtx, id).withId(id).withRev(rev)


class GetCommand(Command):
    stateCtx: StateCtx
    id: StateId
    rev: int
    labels = dict[str, str]

    def __init__(self, stateCtx: StateCtx, stateId: StateId):
        self.stateCtx = stateCtx
        self.stateId = stateId
        self.id: StateId
        self.rev: int

    def withId(self, id: StateId) -> "GetCommand":
        self.labels = dict[str, str]
        self.id = id
        return self

    def withRev(self, rev: int) -> "GetCommand":
        self.rev = rev
        return self

    def withLabels(self, labels: dict[str, str]) -> "GetCommand":
        self.id = StateId("")
        self.rev = 0
        self.labels = labels

        return self
