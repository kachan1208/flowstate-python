from state import StateCtx, State, StateAnnotation
from command import Command
from transition import Transition
from cmd_pause import paused
from utils import time_rfc3339micro
from datetime import timedelta

DelayAtAnnotation = "flowstate.delay.at"
DelayDurationAnnotation = "flowstate.delay.duration"
DelayCommitAnnotation = "flowstate.delay.commit"


def delayed(state: State) -> bool:
    return state.transition.annotations[DelayAtAnnotation] != ""


def delay(state_ctx: StateCtx, dur: float) -> "DelayCommand":
    return DelayCommand(state_ctx=state_ctx, duration=dur)


class DelayCommand(Command):
    def __init__(
        self,
        state_ctx: StateCtx = None,
        delay_state_ctx: StateCtx = None,
        duration: float = 0,
        commit: bool = False,
    ):
        self.state_ctx: StateCtx = state_ctx
        self.delay_state_ctx: StateCtx = delay_state_ctx
        self.duration: float = duration
        self.commit: bool = commit

    def with_commit(self, commit: bool) -> "DelayCommand":
        self.commit = commit
        return self

    def prepare(self):
        delayed_state_ctx = self.state_ctx.copy_to(StateCtx())
        delayed_state_ctx.transitions.append(delayed_state_ctx.current.transition)

        next_ts = Transition(
            from_id=delayed_state_ctx.current.transition.to_id,
            to_id=delayed_state_ctx.current.transition.to_id,
            annotations={},
        )

        if paused(delayed_state_ctx.current):
            next_ts.set_annotation(StateAnnotation, "resumed")

        next_ts.set_annotation(DelayAtAnnotation, time_rfc3339micro())
        next_ts.set_annotation(DelayDurationAnnotation, str(self.duration))
        next_ts.set_annotation(DelayCommitAnnotation, str(self.commit))

        delayed_state_ctx.current.transition = next_ts
        self.delay_state_ctx = delayed_state_ctx
