from memdriver.registry import FlowRegistry
from memdriver.driver import Driver


def test_single_node():
    driver = Driver()
    flow_registry = driver.flow_registry

    def first(state_ctx, e) -> Command:
        Track()

    flow_registry.set_flow(
        "first",
    )
