from cmd_transit import transit
from flow import FlowId, FlowFunc
from memdriver.driver import Driver
from state import StateCtx, State
from testcases.tracker import Tracker, track
from engine import Engine
from cmd_end import end


def test_condition():
    driver = Driver()
    tracker = Tracker()
    flow_registry = driver.flow_registry

    def first(state_ctx: StateCtx, _: Engine):
        track(state_ctx, tracker)

        bID = FlowId("third")
        if state_ctx.current.annotations["condition"] == "True":
            bID = FlowId("second")

        return transit(state_ctx, bID)

    flow_registry.set_flow(
        "first",
        FlowFunc(first),
    )

    def second(state_ctx: StateCtx, _: Engine):
        track(state_ctx, tracker)

        return end(state_ctx)

    flow_registry.set_flow(
        "second",
        FlowFunc(second),
    )

    def third(state_ctx: StateCtx, _: Engine):
        track(state_ctx, tracker)

        return end(state_ctx)

    flow_registry.set_flow(
        "third",
        FlowFunc(third),
    )

    with Engine(driver) as e:
        state_ctx_true: StateCtx = StateCtx(
            current=State(
                id="aTrueTID",
                annotations={"condition": "True"},
            ),
        )
        e.do(transit(state_ctx_true, "first"))
        e.execute(state_ctx_true)

        assert tracker.visited == ["first", "second"]

        state_ctx_false: StateCtx = StateCtx(
            current=State(
                id="aFalseTID",
                annotations={"condition": "False"},
            ),
        )
        e.do(transit(state_ctx_false, "first"))
        e.execute(state_ctx_false)

        assert tracker.visited == ["first", "second", "first", "third"]
