from state import StateCtx
from command import Command
from doer import Doer, ErrCommandNotSupported


def noop(state_ctx: StateCtx) -> "NoopCommand":
    return NoopCommand(state_ctx)


class NoopCommand(Command):
    state_ctx: StateCtx

    def __init__(self, state_ctx: StateCtx):
        self.state_ctx = state_ctx


class DefaultNoopDoer(Doer):
    async def do(self, cmd: Command):
        if not isinstance(cmd, NoopCommand):
            raise ErrCommandNotSupported
