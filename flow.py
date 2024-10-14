from command import Command
from state import StateCtx
from engine import Engine


FlowId = str


class Flow:
    def execute(self, stateCtx: StateCtx, e: Engine) -> Command:
        pass


def FlowFunc(func):
    def execute(stateCtx: StateCtx, e: Engine) -> Command:
        return func(stateCtx, e)

    return execute
