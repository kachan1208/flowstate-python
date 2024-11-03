from flow import FlowFunc
from memdriver.driver import Driver
from command import Command
from state import StateCtx, State
from engine import Engine
from testcases.tracker import track, Tracker
from cmd_end import end
from cmd_transit import transit


def test_three_consequent_nodes():
    driver = Driver()
    flow_registry = driver.flow_registry
    tracker = Tracker()

    def first(state_ctx: StateCtx, _: Engine) -> Command:
        track(state_ctx, tracker)
        return transit(state_ctx, "second")

    flow_registry.set_flow("first", FlowFunc(first))

    def second(state_ctx: StateCtx, _: Engine) -> Command:
        track(state_ctx, tracker)
        return transit(state_ctx, "third")

    flow_registry.set_flow("second", FlowFunc(second))

    def third(state_ctx: StateCtx, _: Engine) -> Command:
        track(state_ctx, tracker)
        return end(state_ctx)

    flow_registry.set_flow("third", FlowFunc(third))

    with Engine(driver) as e:
        state_ctx = StateCtx(current=State(id="aTID", rev=0))
        e.do(transit(state_ctx, "first"))
        e.execute(state_ctx)

    assert tracker.visited == ["first", "second", "third"]