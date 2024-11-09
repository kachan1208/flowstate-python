from flow import FlowId
from flow import Flow
from engine import ErrFlowNotFound
from doer import Doer, ErrCommandNotSupported
from command import Command
from cmd_get_flow import GetFlowCommand


class FlowRegistry(Doer):
    def __init__(self, flows: dict[FlowId, Flow] = None):
        self.flows: dict[FlowId, Flow] = flows
        if self.flows is None:
            self.flows = {}

    def set_flow(self, id: FlowId, flow: Flow):
        self.flows[id] = flow

    def flow(self, id: FlowId) -> Flow:
        if id in self.flows:
            return self.flows[id]

        raise ErrFlowNotFound


class FlowGetter(Doer):
    def __init__(self, flow_registry: FlowRegistry):
        self.flow_registry = flow_registry

    async def do(self, cmd: Command) -> None:
        if not isinstance(cmd, GetFlowCommand):
            raise ErrCommandNotSupported

        if cmd.state_ctx.current.transition.to_id == "":
            raise Exception("transition flow is empty")

        try:
            f = self.flow_registry.flow(cmd.state_ctx.current.transition.to_id)
            cmd.flow = f
        except Exception as e:
            raise e
