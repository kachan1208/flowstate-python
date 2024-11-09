from data import Data, DataId
from state import State, StateCtx
from datetime import datetime
from queue import Queue
from transition import Transition
from itertools import groupby


class Log:
    def __init__(
        self,
        rev: int = 0,
        entries: list[StateCtx] = None,
        changes: list[StateCtx] = None,
        listeners: list[Queue] = None,
    ):
        self.rev: int = rev
        self.entries: list[StateCtx] = entries
        if self.entries is None:
            self.entries = []

        self.changes: list[StateCtx] = changes
        if self.changes is None:
            self.changes = []

        self.listeners: list[Queue] = listeners
        if self.listeners is None:
            self.listeners = []

    def append(self, state_ctx: StateCtx):
        commited_t, _ = self.get_latest_by_id(state_ctx.current.id)
        if commited_t is None:
            commited_t = StateCtx()

        state_ctx.copy_to(commited_t)
        commited_t.current.set_commited_at(datetime.now())
        commited_t.current.copy_to(commited_t.commited)
        commited_t.transitions = []

        self.rev += 1
        commited_t.commited.rev = self.rev
        commited_t.current.rev = self.rev

        self.changes.append(commited_t)

        commited_t.commited.copy_to(state_ctx.current)
        commited_t.commited.copy_to(state_ctx.commited)
        state_ctx.transitions = []

    def commit(self):
        sorted_changes = sorted(self.changes, key=lambda x: x.current.id)
        self.changes = [
            next(group)
            for _, group in groupby(sorted_changes, key=lambda x: x.current.id)
        ]

        self.changes = sorted(self.changes, key=lambda x: x.current.rev)
        for stateCtx in self.changes:
            self.entries.append(stateCtx)

        rev = 0
        if len(self.entries) > 0:
            rev = self.entries[-1].current.rev

        self.changes = []
        for q in self.listeners:
            if q.full():
                q.get()

            q.put(rev)

    def rollback(self):
        self.changes = []

    def get_latest_by_id(self, id: DataId) -> ("StateCtx", int):
        if len(self.entries) == 0:
            return None, 0

        for e in reversed(self.entries):
            if e.commited.id == id:
                return e.copy_to(StateCtx()), e.commited.rev

        return None, 0

    def get_by_id_and_rev(self, id: DataId, rev: int) -> "StateCtx":
        for e in self.entries:
            if e.commited.id == id and e.commited.rev == rev:
                return e.copy_to(StateCtx())

        return None

    def get_latest_by_labels(self, labels: list[dict[str, str]]) -> ("StateCtx", int):
        for e in reversed(self.entries):
            if match_labels(e.commited, labels):
                return e.copy_to(StateCtx()), e.commited.rev

        return None, 0

    def entries(self, since: int, limit: int) -> (list["StateCtx"], int):
        if limit == 0:
            return None, since

        entries: list[StateCtx] = []
        for e in self.entries:
            if e.commited.rev <= since:
                continue

            entries.append(e.copy_to(StateCtx()))
            since = e.commited.rev
            if len(entries) == limit:
                break

        return entries, since

    def subscribe_commit(self, q: Queue):
        self.listeners.append(q)

    def unsubscribe_commit(self, q: Queue):
        self.listeners.remove(q)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()


def match_labels(state: "State", or_labels: list[dict[str, str]]) -> bool:
    if len(or_labels) == 0:
        return True

    if len(state.labels) == 0:
        return False

    for labels in or_labels:
        found: bool = True

        for k, v in labels.items():
            label = state.labels.get(k)
            if label is None or label != v:
                found = False

        if not found:
            continue

        return True

    return False
