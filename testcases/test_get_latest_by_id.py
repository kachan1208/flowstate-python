from cmd_commit import commit, commit_state_ctx
from cmd_get import get_by_id
from memdriver.driver import Driver
from state import StateCtx, State
from engine import Engine


def test_get_latest_by_id():
    driver = Driver()
    e = Engine(driver)

    state_ctx = StateCtx(current=State(id="aTID"))
    state_ctx.current.set_annotation("v", "1")
    e.do(commit(commit_state_ctx(state_ctx)))

    state_ctx.current.set_annotation("v", "2")
    e.do(commit(commit_state_ctx(state_ctx)))

    state_ctx.current.set_annotation("v", "3")
    e.do(commit(commit_state_ctx(state_ctx)))
    expected_state_ctx: StateCtx = state_ctx.copy_to(StateCtx())

    found_state_ctx: StateCtx = StateCtx()
    e.do(
        get_by_id(
            found_state_ctx,
            "aTID",
            0,
        )
    )

    assert expected_state_ctx.current.annotations == found_state_ctx.current.annotations
    assert expected_state_ctx.current.id == found_state_ctx.current.id
    assert expected_state_ctx.current.rev == found_state_ctx.current.rev
    assert expected_state_ctx.current.labels == found_state_ctx.current.labels

    assert (
        expected_state_ctx.commited.annotations == found_state_ctx.commited.annotations
    )
    assert expected_state_ctx.commited.id == found_state_ctx.commited.id
    assert expected_state_ctx.commited.rev == found_state_ctx.commited.rev
    assert expected_state_ctx.commited.labels == found_state_ctx.commited.labels

    assert expected_state_ctx.transitions == found_state_ctx.transitions
