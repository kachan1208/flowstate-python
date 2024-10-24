from command import Command
from engine import Engine
from memdriver.data_log import DataLog
from memdriver.registry import FlowRegistry, FlowGetter
from memdriver.log import Log
from doer import Doer, ErrCommandNotSupported
from cmd_transit import DefaultTransitDoer
from cmd_pause import DefaultPauseDoer
from cmd_resume import DefaultResumeDoer
from cmd_end import DefaultEndDoer
from cmd_noop import DefaultNoopDoer
from cmd_serialize import DefaultSerializerDoer
from cmd_deserialize import DefaultDeserializeDoer
from cmd_dereference_data import DefaultDereferenceDataDoer
from cmd_reference_data import DefaultReferenceDataDoer


class Driver:
    l: Log
    doers: list[Doer]
    flow_registry: FlowRegistry

    def __init__(self):
        self.l = Log()
        self.flow_registry = FlowRegistry()

        self.doers = [
            DefaultTransitDoer,
            DefaultPauseDoer,
            DefaultResumeDoer,
            DefaultEndDoer,
            DefaultNoopDoer,
            DefaultSerializerDoer,
            DefaultDeserializeDoer,
            DefaultDereferenceDataDoer,
            DefaultReferenceDataDoer,
            DataLog(),
            FlowGetter(self.flow_registry),
        ]

    def do(self, cmd: Command):
        for doer in self.doers:
            try:
                doer.do(cmd)
            except ErrCommandNotSupported:
                continue
            except Exception as e:
                raise Exception(f"{doer} do: {e}")

    def init(self, e: Engine):
        for doer in self.doers:
            try:
                doer.init(e)
            except Exception as e:
                raise Exception(f"{doer} init: {e}")

    def shutdown(self):
        for doer in self.doers:
            try:
                doer.shutdown()
            except Exception as e:
                raise Exception(f"{doer} shutdown: {e}")
