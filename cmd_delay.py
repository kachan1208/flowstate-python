from state import StateCtx, State, StateAnnotation
from command import Command
from transition import Transition
from cmd_pause import Paused
from utils import time_rfc3339micro
from datetime import timedelta

DelayAtAnnotation = "flowstate.delay.at"
DelayDurationAnnotation = "flowstate.delay.duration"
DelayCommitAnnotation = "flowstate.delay.commit"


def Delayed(state: State) -> bool:
    return state.transition.annotations[DelayAtAnnotation] != ""


def Delay(stateCtx: StateCtx, dur: timedelta) -> "DelayCommand":
    return DelayCommand(stateCtx, dur)


class DelayCommand(Command):
    stateCtx: StateCtx
    delayStateCtx: StateCtx
    duration: timedelta
    commit: bool

    def __init__(
        self,
        stateCtx: StateCtx,
        delayStateCtx: StateCtx,
        duration: timedelta,
        commmit: bool,
    ):
        self.stateCtx = stateCtx
        self.delayStateCtx = delayStateCtx
        self.duration = duration
        self.commit = commmit

    def withCommit(self, commit: bool) -> "DelayCommand":
        self.commit = commit
        return self

    def prepare(self):
        delayedStateCtx = self.stateCtx.copyTo(StateCtx())
        delayedStateCtx.transitions.append(delayedStateCtx.current.transition)

        nextTs = Transition(
            fromId=delayedStateCtx.current.transition.toId,
            toId=delayedStateCtx.current.transition.toId,
            annotations={},
        )

        if Paused(delayedStateCtx.current):
            nextTs.setAnnotation(StateAnnotation, "resumed")

        nextTs.setAnnotation(DelayAtAnnotation, time_rfc3339micro())
        nextTs.setAnnotation(DelayDurationAnnotation, self.duration)
        nextTs.setAnnotation(DelayCommitAnnotation, self.commit)

        delayedStateCtx.current.transition = nextTs
        self.delayStateCtx = delayedStateCtx
