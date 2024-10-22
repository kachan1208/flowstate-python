from command import Command
from state import StateCtx
from engine import Engine


FlowId = str


class Flow:
    def execute(self, state_ctx: StateCtx, e: Engine) -> Command:
        pass


def flow_func(func):
    def execute(state_ctx: StateCtx, e: Engine) -> Command:
        return func(state_ctx, e)

    return execute
