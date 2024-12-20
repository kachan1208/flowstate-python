from cmd_commit import commit, commit_state_ctx
from cmd_get import get_by_labels
from memdriver.driver import Driver
from state import StateCtx, State
from engine import Engine


import pytest


@pytest.mark.asyncio
async def test_get_latest_by_label():
    driver = Driver()
    e = Engine(driver)

    state_ctx = StateCtx(current=State(id="aTID", labels={"foo": "fooVal"}))
    state_ctx.current.set_annotation("v", "1")
    await e.do(commit(commit_state_ctx(state_ctx)))

    state_ctx.current.set_annotation("v", "2")
    await e.do(commit(commit_state_ctx(state_ctx)))

    state_ctx.current.set_annotation("v", "3")
    await e.do(commit(commit_state_ctx(state_ctx)))
    expected_state_ctx: StateCtx = state_ctx.copy_to(StateCtx())

    found_state_ctx: StateCtx = StateCtx()
    await e.do(get_by_labels(found_state_ctx, {"foo": "fooVal"}))

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
