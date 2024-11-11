from cmd_reference_data import reference_data
from cmd_store_data import store_data
from state import State, StateCtx
from data import Data
from memdriver.driver import Driver
from testcases.tracker import Tracker, track
from command import Command
from engine import Engine
from cmd_dereference_data import dereference_data
from cmd_get_data import get_data
from cmd_transit import transit
from cmd_end import end
from cmd_execute import execute
from flow import FlowFunc


import pytest


@pytest.mark.asyncio
async def test_data_store_get():
    tracker = Tracker()

    driver = Driver()
    flow_registry = driver.flow_registry

    async def store(state_ctx: StateCtx, e: Engine) -> "Command":
        track(state_ctx, tracker)

        d = Data(
            id="aTID",
            b=bytearray(b"foo"),
        )

        await e.do(
            store_data(d),
            reference_data(
                state_ctx=state_ctx,
                data=d,
                annotation="aDataKey",
            ),
            transit(state_ctx, "get"),
        )

        return execute(state_ctx)

    flow_registry.set_flow("store", FlowFunc(store))

    act_data = Data()

    async def get(state_ctx: StateCtx, e: Engine) -> "Command":
        track(state_ctx, tracker)

        await e.do(
            dereference_data(
                state_ctx=state_ctx,
                data=act_data,
                annotation="aDataKey",
            ),
            get_data(d=act_data),
            transit(state_ctx, "finish"),
        )

        return execute(state_ctx)

    flow_registry.set_flow("get", FlowFunc(get))

    async def finish(state_ctx: StateCtx, _: Engine) -> Command:
        track(state_ctx, tracker)

        return end(state_ctx)

    flow_registry.set_flow("finish", FlowFunc(finish))

    exp_data = Data(
        id="aTID",
        rev=1,
        b=bytearray(b"foo"),
    )

    ctx = StateCtx(current=State(id="aTID"))
    with Engine(driver) as e:
        await e.do(transit(ctx, "store"))
        await e.do(execute(ctx))

        await tracker.wait_visited_equal(["store", "get", "finish"], 2)
        assert exp_data.id == act_data.id
        assert exp_data.rev == act_data.rev
        assert exp_data.b == act_data.b
