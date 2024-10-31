from idlelib.pyparse import trans

from state import StateCtx, State
from transition import Transition


def test_StateCtx_copy_to():
    transition = Transition()
    ctx: StateCtx = StateCtx(
        current=State(rev=10), commited=State(rev=10), transitions=[transition]
    )
    ctx_copy = ctx.copy_to(StateCtx())

    assert ctx != ctx_copy
    assert len(ctx_copy.transitions) == 1
    assert ctx_copy.transitions != [transition]
    assert ctx.current != ctx_copy.current
    assert ctx.commited != ctx_copy.commited


def test_State_copy_to():
    state = State(
        id="id",
        rev=5,
        annotations={"key": "value"},
        labels={"key": "value"},
        commited_at_unix_milli=10,
        transition=Transition(),
    )

    state_copy = state.copy_to(State())
    assert state != state_copy

    state_copy.id = "id_copy"
    state_copy.rev = 6
    state_copy.annotations = {"key2": "value2"}
    state_copy.labels = {"key2": "value2"}

    assert state.id != state_copy.id
    assert state.rev != state_copy.rev
    assert state.annotations != state_copy.annotations
    assert state.labels != state_copy.labels
