from state import StateCtx
from flow import FlowId
from command import Command
from doer import Doer, ErrCommandNotSupported
from transition import Transition

def transit(state_ctx: StateCtx, fId: FlowId) -> "TransitCommand":
    return TransitCommand(state_ctx, fId)

class TransitCommand(Command):
    def __init__(self, state_ctx: StateCtx, f_id: FlowId):
        self.state_ctx = state_ctx
        self.flowId = f_id

    def committable_state_ctx(self) -> StateCtx:
        return self.state_ctx

class DefaultTransitDoer(Doer):
    def do(self, cmd: Command):
        if cmd is not TransitCommand:
            raise ErrCommandNotSupported

        if cmd.flowId == "":
            raise Exception("flow id empty")

        cmd.state_ctx.transitions.append(cmd.state_ctx.current.transition)
        nextTs = Transition(
            from_id=cmd.state_ctx.current.transition.to_id,
            to_id=cmd.flowId,
            annotations={},
        )

        cmd.state_ctx.current.transition = nextTs
