from cmd_commit import commit, commit_state_ctx
from cmd_get import get_by_id
from flow import FlowFunc
from memdriver.registry import FlowRegistry
from memdriver.driver import Driver
from command import Command
from state import StateCtx, State
from engine import Engine
from testcases.tracker import track, Tracker
from cmd_end import end
from cmd_transit import transit


def test_get_by_id_and_rev():
    driver = Driver()
    e = Engine(driver)

    state_ctx = StateCtx(current=State(id="aTID"))
    state_ctx.current.set_annotation("v", "1")
    e.do(commit(commit_state_ctx(state_ctx)))

    expected_state_ctx: StateCtx = state_ctx.copy_to(StateCtx())

    state_ctx.current.set_annotation("v", "2")
    e.do(commit(commit_state_ctx(state_ctx)))

    state_ctx.current.set_annotation("v", "3")
    e.do(commit(commit_state_ctx(state_ctx)))

    found_state_ctx: StateCtx = StateCtx()
    e.do(
        get_by_id(
            found_state_ctx,
            "aTID",
            expected_state_ctx.commited.rev,
        )
    )

    assert expected_state_ctx.commited.id == found_state_ctx.commited.id
