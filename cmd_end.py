from state import StateCtx, State, StateAnnotation
from doer import Doer
from command import Command, ErrCommandNotSupported
from transition import Transition


class EndCommand(Command):
    def __init__(self, stateCtx: StateCtx) -> None:
        self.stateCtx = stateCtx

    def commitableStateCtx(self) -> StateCtx:
        return self.stateCtx


class DefaultEndDoer(Doer):
    def do(self, cmd: Command) -> None:
        if cmd is not EndCommand:
            raise ErrCommandNotSupported

        cmd.stateCtx.transitions.append(cmd.stateCtx.current.transition)
        nextTs = Transition(
            fromId=cmd.stateCtx.current.transition.toId,
            toId="",
            annotations={},
        )

        nextTs.setAnnotation(StateAnnotation, "ended")
        cmd.stateCtx.current.transition = nextTs


def Ended(state: State) -> bool:
    return state.Transition.Annotations[StateAnnotation] == "ended"


def End(stateCtx: StateCtx) -> EndCommand:
    return EndCommand(stateCtx)
