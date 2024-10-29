from data import Data, DataId
from state import StateCtx
from datetime import datetime
from queue import Queue
from transition import Transition
from itertools import groupby


class Log:
    def __init__(
        self,
        rev: int = 0,
        entries: list[StateCtx] = [],
        changes: list[StateCtx] = [],
        listeners: list[Queue] = [],
    ):
        self.rev: int = rev
        self.entries: list[StateCtx] = entries
        self.changes: list[StateCtx] = changes
        self.listeners: list[Queue] = listeners

    def append(self, state_ctx: StateCtx):
        commited_t, _ = self.get_latest_by_id(state_ctx.current.id)
        if commited_t is None:
            commited_t = StateCtx()

        state_ctx.copy_to(commited_t)
        commited_t.current.set_commited_at(datetime.now())
        commited_t.current.copy_to(commited_t.commited)
        commited_t.transitions = list[Transition]

        self.rev += 1
        commited_t.commited.rev = self.rev
        commited_t.current.rev = self.rev

        self.changes.append(commited_t)

        commited_t.commited.copy_to(state_ctx.current)
        commited_t.commited.copy_to(state_ctx.commited)
        state_ctx.transitions = list[Transition]

    def commit(self):
        sorted_changes = sorted(self.changes, key=lambda x: x.current.id)
        self.changes = [
            next(group)
            for _, group in groupby(sorted_changes, key=lambda x: x.current.id)
        ]

        self.changes = sorted(self.changes, key=lambda x: x.current.rev)
        for _, stateCtx in self.changes:
            self.entries.append(stateCtx)

        rev = 0
        if len(self.entries) > 0:
            rev = self.entries[-1].current.rev

        self.changes = list[StateCtx]
        for q in self.listeners:
            if q.full():
                q.get()

            q.put(rev)

    def rollback(self):
        self.changes = list[StateCtx]

    def get_latest_by_id(self, id: DataId) -> ("StateCtx", int):
        for e in reversed(self.entries):
            if e.commited.id == id:
                return e.copy_to(StateCtx()), e.commited.rev

    def get_by_id_and_rev(self, id: DataId, rev: int) -> "StateCtx":
        for e in self.entries:
            if e.commited.id == id and e.commited.rev == rev:
                return e.copy_to(StateCtx())

    def get_latest_by_labels(self, labels: list[str]) -> (Data, int):
        pass

    def subscribe_commit(self, q: Queue):
        self.listeners.append(q)
