from unittest import TestCase
from memdriver.registry import Registry
from flow import FlowFunc
from state import StateCtx
from engine import Engine
from command import Command
from cmd_end import End


class TestSingleNode(TestCase):
    def setUp(self):
        return super().setUp()

    def test_single_node(self):
        @FlowFunc
        def flow(stateCtx: StateCtx, e: Engine) -> Command:
            return End(stateCtx)

        self.registry.setFlow("flow1", flow)

        Engine()
