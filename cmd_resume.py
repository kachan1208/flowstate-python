from state import StateCtx, State, StateAnnotation
from command import Command
from doer import Doer, ErrCommandNotSupported
from transition import Transition


def resumed(state: State) -> bool:
    return state.transition.annotations.get(StateAnnotation) == "resumed"


def resume(state_ctx: StateCtx) -> "ResumeCommand":
    return ResumeCommand(state_ctx)


class ResumeCommand(Command):
    state_ctx: StateCtx

    def __init__(self, state_ctx: StateCtx):
        self.state_ctx = state_ctx

    def committable_state_ctx(self) -> StateCtx:
        return self.state_ctx


class DefaultResumeDoer(Doer):
    def do(self, cmd: Command) -> None:
        if not isinstance(cmd, ResumeCommand):
            raise ErrCommandNotSupported

        cmd.state_ctx.transitions.append(cmd.state_ctx.current.transition)
        nextTs = Transition(
            from_id=cmd.state_ctx.current.transition.to_id,
            to_id=cmd.state_ctx.current.transition.to_id,
            annotations={},
        )

        nextTs.set_annotation(StateAnnotation, "resumed")
        cmd.state_ctx.current.transition = nextTs
