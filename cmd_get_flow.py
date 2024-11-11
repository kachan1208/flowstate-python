from command import Command
from state import StateCtx
from flow import Flow


class GetFlowCommand(Command):
    def __init__(self, state_ctx: StateCtx):
        self.state_ctx: StateCtx = state_ctx
        self.flow: Flow | None = None

    def cmd(self):
        pass


def get_flow(state_ctx: StateCtx) -> GetFlowCommand:
    cmd = GetFlowCommand(state_ctx)
    return cmd
