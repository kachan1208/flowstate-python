import asyncio

from cmd_deserialize import deserialize
from memdriver.driver import Driver
from state import State, StateCtx
from engine import Engine
from command import Command
from testcases.tracker import Tracker, track
from cmd_resume import resumed
from cmd_transit import transit
from cmd_pause import pause
from cmd_serialize import serialize
from cmd_execute import execute
from cmd_noop import noop
from cmd_resume import resume
from cmd_end import end
from flow import FlowFunc


def test_call_flow():
    tracker = Tracker()
    close_event = asyncio.Event()

    driver = Driver()
    flow_registry = driver.flow_registry

    def call(state_ctx: StateCtx, e: Engine) -> "Command":
        track(state_ctx, tracker)

        if resumed(state_ctx.current):
            return transit(state_ctx, "call_end")

        next_state_ctx = StateCtx(current=State(id="aTID"))

        e.do(
            pause(state_ctx),
            serialize(state_ctx, next_state_ctx, "caller_state"),
            transit(next_state_ctx, "called"),
            execute(next_state_ctx),
        )

        return noop(state_ctx)

    flow_registry.set_flow("call", FlowFunc(call))

    def called(state_ctx: StateCtx, e: Engine) -> "Command":
        track(state_ctx, tracker)

        return transit(state_ctx, "called_end")

    flow_registry.set_flow("called", FlowFunc(called))

    def called_end(state_ctx: StateCtx, e: Engine) -> "Command":
        track(state_ctx, tracker)

        if state_ctx.current.annotations["caller_state"] != "":
            call_state_ctx = StateCtx()
            e.do(
                deserialize(state_ctx, call_state_ctx, "caller_state"),
                resume(call_state_ctx),
                execute(call_state_ctx),
                end(state_ctx),
            )

            return noop(state_ctx)

        return end(state_ctx)

    flow_registry.set_flow("called_end", FlowFunc(called_end))

    def call_end(state_ctx: StateCtx, _: Engine) -> "Command":
        track(state_ctx, tracker)

        close_event.set()

        return end(state_ctx)

    flow_registry.set_flow("call_end", FlowFunc(call_end))

    with Engine(driver) as e:
        state_ctx = StateCtx(current=State(id="aTID"))

        e.do(transit(state_ctx, "call"))
        e.execute(state_ctx)

        close_event.wait()

    assert tracker.visited == ["call", "called", "called_end", "call", "call_end"]
