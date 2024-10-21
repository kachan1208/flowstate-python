from state import StateCtx, State, StateAnnotation
from command import Command
from doer import Doer, ErrCommandNotSupported
from transition import Transition


def Resumed(state: State) -> bool:
    return state.transition.annotations[StateAnnotation] == "resumed"


def Resume(stateCtx: StateCtx) -> "ResumeCommand":
    return ResumeCommand(stateCtx)


class ResumeCommand(Command):
    stateCtx: StateCtx

    def __init__(self, stateCtx: StateCtx):
        self.stateCtx = stateCtx

    def committableStateCtx(self) -> StateCtx:
        return self.stateCtx


class DefaultResumeDoer(Doer):
    def do(self, cmd: Command) -> None:
        if cmd is not ResumeCommand:
            raise ErrCommandNotSupported

        cmd.stateCtx.transitions.append(cmd.stateCtx.current.transition)
        nextTs = Transition(
            fromId=cmd.stateCtx.current.transition.toId,
            toId=cmd.stateCtx.current.transition.toId,
            annotations={},
        )

        nextTs.setAnnotation(StateAnnotation, "resumed")
        cmd.stateCtx.current.transition = nextTs
