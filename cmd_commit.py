from abc import ABC, abstractmethod
from command import Command
from state import StateCtx


class CommitCommand(Command):
    def __init__(self, *cmds: Command):
        self.commands = cmds


class CommitableCommand(ABC):
    @abstractmethod
    def commitableStateCtx(self) -> StateCtx:
        pass


class CommitStateCtxCommand(Command):
    def __init__(self, stateCtx: StateCtx):
        self.stateCtx = stateCtx

    def commitableStateCtx(self) -> StateCtx:
        return self.stateCtx


def Commit(*cmds: Command) -> CommitCommand:
    return CommitCommand(cmds)
