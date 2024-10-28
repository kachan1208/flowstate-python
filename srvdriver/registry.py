from flow import FlowId
from flow import Flow
from engine import ErrFlowNotFound
from doer import Doer, ErrCommandNotSupported
from command import Command
from cmd_get_flow import GetFlowCommand


class FlowRegistry(Doer):
    flows = dict[FlowId, Flow]

    def __init__(self, flows: dict[FlowId, Flow]):
        self.flows = flows

    def do(self, cmd: Command) -> None:
        if not isinstance(cmd, GetFlowCommand):
            raise ErrCommandNotSupported

        if cmd.state_ctx.current.transition.to_id == "":
            raise Exception("transition flow is empty")

        try:
            f = self.flow(cmd.state_ctx.current.transition.to_id)
            cmd.flow = f
        except Exception as e:
            raise e

    def setFlow(self, id: FlowId, flow: Flow):
        self.flows[id] = flow

    def flow(self, id: FlowId) -> Flow:
        if id in self.flows:
            return self.flows[id]

        raise ErrFlowNotFound
