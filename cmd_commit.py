from command import Command
from state import StateCtx


class CommitCommand(Command):
    def __init__(self, *cmds: Command):
        self.commands = cmds


class CommittableCommand():
    def committableStateCtx(self) -> StateCtx:
        pass


class CommitStateCtxCommand(Command):
    def __init__(self, stateCtx: StateCtx):
        self.stateCtx = stateCtx

    def committableStateCtx(self) -> StateCtx:
        return self.stateCtx


def Commit(*cmds: Command) -> CommitCommand:
    return CommitCommand(cmds)
