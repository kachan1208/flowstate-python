from command import Command
from state import StateCtx


def commit(*cmds: Command) -> "CommitCommand":
    return CommitCommand(*cmds)


class CommittableCommand:
    def committable_state_ctx(self) -> StateCtx:
        pass


class CommitCommand(Command):
    def __init__(self, *cmds: Command):
        self.commands: [Command] = list(cmds)


def commit_state_ctx(state_ctx: StateCtx) -> "CommitStateCtxCommand":
    return CommitStateCtxCommand(state_ctx)


class CommitStateCtxCommand(Command):
    def __init__(self, state_ctx: StateCtx):
        self.state_ctx = state_ctx

    def committable_state_ctx(self) -> StateCtx:
        return self.state_ctx
