from state import StateCtx
from flow import FlowId
from command import Command
from doer import Doer, ErrCommandNotSupported
from transition import Transition

def Transit(stateCtx: StateCtx, fId: FlowId) -> "TransitCommand":
    return TransitCommand(stateCtx, fId)

class TransitCommand(Command):
    def __init__(self, stateCtx: StateCtx, fId: FlowId):
        self.stateCtx = stateCtx
        self.flowId = fId

    def commitableStateCtx(self) -> StateCtx:
        return self.stateCtx

class DefaultTransitDoer(Doer):
    def do(self, cmd: Command):
        if cmd is not TransitCommand:
            raise ErrCommandNotSupported

        if cmd.flowId == "":
            raise Exception("flow id empty")

        cmd.stateCtx.transitions.append(cmd.stateCtx.current.transition)
        nextTs = Transition(
            fromId=cmd.stateCtx.current.transition.toId,
            toId=cmd.flowId,
            annotations={},
        )

        cmd.stateCtx.current.transition = nextTs
