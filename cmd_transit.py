from state import StateCtx
from flow import FlowId
from command import Command
from cmd_commit import CommittableCommand
from doer import Doer, ErrCommandNotSupported
from transition import Transition


def transit(state_ctx: StateCtx, f_id: FlowId) -> "TransitCommand":
    return TransitCommand(state_ctx, f_id)


class TransitCommand(Command, CommittableCommand):
    def __init__(self, state_ctx: StateCtx, f_id: FlowId):
        self.state_ctx = state_ctx
        self.flow_id = f_id

    def committable_state_ctx(self) -> StateCtx:
        return self.state_ctx


class DefaultTransitDoer(Doer):
    async def do(self, cmd: Command):
        if not isinstance(cmd, TransitCommand):
            raise ErrCommandNotSupported

        if cmd.flow_id == "":
            raise Exception("flow id empty")

        cmd.state_ctx.transitions.append(cmd.state_ctx.current.transition)
        next_ts = Transition(
            from_id=cmd.state_ctx.current.transition.to_id,
            to_id=cmd.flow_id,
            annotations={},
        )

        cmd.state_ctx.current.transition = next_ts
