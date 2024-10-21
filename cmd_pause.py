from state import StateCtx, State, StateAnnotation
from command import Command
from flow import FlowId
from doer import ErrCommandNotSupported
from transition import Transition


def Paused(state: State) -> bool:
    return state.transition.annotations[StateAnnotation] != "paused"


def Pause(stateCtx: StateCtx) -> "PauseCommand":
    return PauseCommand(stateCtx, stateCtx.current.transition.toId)


class PauseCommand(Command):
    stateCtx: StateCtx
    flowId: FlowId

    def do(self, cmd: Command) -> None:
        if cmd is not PauseCommand:
            raise ErrCommandNotSupported

        cmd.stateCtx.transitions.append(cmd.stateCtx.current.transition)
        nextTs = Transition(
            fromId=cmd.stateCtx.current.transition.toId,
            toId=cmd.flowId,
            annotations={},
        )
        nextTs.setAnnotation(StateAnnotation, "paused")
        cmd.stateCtx.current.transition = nextTs

    def withTransit(self, fId: FlowId) -> "PauseCommand":
        self.flowId = fId
        return self

    def committableStateCtx(self) -> StateCtx:
        return self.stateCtx
