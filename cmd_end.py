from state import StateCtx, State, StateAnnotation
from doer import Doer, ErrCommandNotSupported
from command import Command
from transition import Transition


class EndCommand(Command):
    def __init__(self, state_ctx: StateCtx) -> None:
        self.state_ctx = state_ctx

    def committable_state_ctx(self) -> StateCtx:
        return self.state_ctx


class DefaultEndDoer(Doer):
    def do(self, cmd: Command) -> None:
        if cmd is not EndCommand:
            raise ErrCommandNotSupported

        cmd.state_ctx.transitions.append(cmd.state_ctx.current.transition)
        next_ts = Transition(
            from_id=cmd.state_ctx.current.transition.to_id,
            to_id="",
            annotations={},
        )

        next_ts.set_annotation(StateAnnotation, "ended")
        cmd.state_ctx.current.transition = next_ts


def ended(state: State) -> bool:
    return state.transition.annotations[StateAnnotation] == "ended"


def end(state_ctx: StateCtx) -> EndCommand:
    return EndCommand(state_ctx)
