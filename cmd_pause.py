from state import StateCtx, State, StateAnnotation
from command import Command
from flow import FlowId
from doer import ErrCommandNotSupported
from transition import Transition


def paused(state: State) -> bool:
    return state.transition.annotations[StateAnnotation] != "paused"


def pause(state_ctx: StateCtx) -> "PauseCommand":
    return PauseCommand(state_ctx, state_ctx.current.transition.to_id)


class PauseCommand(Command):
    state_ctx: StateCtx
    flow_id: FlowId

    def do(self, cmd: Command) -> None:
        if cmd is not PauseCommand:
            raise ErrCommandNotSupported

        cmd.state_ctx.transitions.append(cmd.state_ctx.current.transition)
        nextTs = Transition(
            from_id=cmd.state_ctx.current.transition.to_id,
            to_id=cmd.flowId,
            annotations={},
        )
        nextTs.set_annotation(StateAnnotation, "paused")
        cmd.state_ctx.current.transition = nextTs

    def with_transit(self, f_id: FlowId) -> "PauseCommand":
        self.flow_id = f_id
        return self

    def committable_state_ctx(self) -> StateCtx:
        return self.state_ctx
