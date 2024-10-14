from state import StateCtx
from command import Command
from doer import Doer, ErrCommandNotSupported


def Noop(stateCtx: StateCtx) -> "NoopCommand":
    return NoopCommand(stateCtx)


class NoopCommand(Command):
    stateCtx: StateCtx

    def __init__(self, stateCtx: StateCtx):
        self.stateCtx = stateCtx


class DefaultNoopDoer(Doer):
    def do(self, cmd: Command):
        if cmd is NoopCommand:
            raise ErrCommandNotSupported
