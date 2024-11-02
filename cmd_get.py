from state import StateCtx, StateId
from command import Command


def get_by_id(state_ctx: StateCtx, id: StateId, rev: int) -> "GetCommand":
    return GetCommand(state_ctx, id).with_id(id).with_rev(rev)


def get_by_labels(state_ctx: StateCtx, labels: dict[str, str]) -> "GetCommand":
    return GetCommand(state_ctx).with_labels(labels)


class GetCommand(Command):
    state_ctx: StateCtx
    id: StateId
    rev: int
    labels: dict[str, str]

    def __init__(self, state_ctx: StateCtx, state_id: StateId = 0):
        self.state_ctx = state_ctx
        self.stateId = state_id
        self.id: StateId
        self.rev: int

    def with_id(self, id: StateId) -> "GetCommand":
        self.labels: dict[str, str] = {}
        self.id = id
        return self

    def with_rev(self, rev: int) -> "GetCommand":
        self.rev = rev
        return self

    def with_labels(self, labels: dict[str, str]) -> "GetCommand":
        self.id = StateId("")
        self.rev = 0
        self.labels = labels

        return self
