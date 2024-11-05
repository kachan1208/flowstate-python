from state import State

recovery_attempt_annotation = "flowstate.recovery.attempt"


def recovery_attempt(state: State) -> int:
    return int(state.transition.annotations.get(recovery_attempt_annotation))
