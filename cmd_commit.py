from command import Command
from state import StateCtx


def Commit(*cmds: Command) -> "CommitCommand":
    return CommitCommand(cmds)

class CommittableCommand:
    def committableStateCtx(self) -> StateCtx:
        pass


class CommitCommand(Command):
    def __init__(self, *cmds: Command):
        self.commands = cmds


class CommitStateCtxCommand(Command):
    def __init__(self, state_ctx: StateCtx):
        self.state_ctx = state_ctx

    def committableStateCtx(self) -> StateCtx:
        return self.state_ctx
