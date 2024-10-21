from state import StateCtx, State, StateAnnotation
from doer import Doer, ErrCommandNotSupported
from command import Command
from transition import Transition


class EndCommand(Command):
    def __init__(self, stateCtx: StateCtx) -> None:
        self.stateCtx = stateCtx

    def committableStateCtx(self) -> StateCtx:
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
    return state.transition.annotations[StateAnnotation] == "ended"


def End(stateCtx: StateCtx) -> EndCommand:
    return EndCommand(stateCtx)
