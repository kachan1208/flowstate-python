from state import StateCtx
from command import Command


class ExecuteCommand(Command):
    def __init__(self, state_ctx: StateCtx):
        self.sync: bool = False
        self.state_ctx = state_ctx


def execute(state_ctx: StateCtx) -> ExecuteCommand:
    return ExecuteCommand(state_ctx)
