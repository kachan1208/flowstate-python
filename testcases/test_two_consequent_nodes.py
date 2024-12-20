from flow import FlowFunc
from memdriver.driver import Driver
from command import Command
from state import StateCtx, State
from engine import Engine
from testcases.tracker import track, Tracker
from cmd_end import end
from cmd_transit import transit


import pytest


@pytest.mark.asyncio
async def test_two_consequent_nodes():
    driver = Driver()
    flow_registry = driver.flow_registry
    tracker = Tracker()

    async def first(state_ctx: StateCtx, _: Engine) -> Command:
        track(state_ctx, tracker)
        return transit(state_ctx, "second")

    flow_registry.set_flow("first", FlowFunc(first))

    async def second(state_ctx: StateCtx, _: Engine) -> Command:
        track(state_ctx, tracker)
        return end(state_ctx)

    flow_registry.set_flow("second", FlowFunc(second))

    with Engine(driver) as e:
        state_ctx = StateCtx(current=State(id="aTID", rev=0))
        await e.do(transit(state_ctx, "first"))
        await e.execute(state_ctx)

    assert tracker.visited == ["first", "second"]
