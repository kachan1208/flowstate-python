from contextlib import ExitStack

from command import Command
from engine import Engine
from memdriver.data_log import DataLog
from memdriver.getter import Getter
from memdriver.registry import FlowRegistry, FlowGetter
from memdriver.log import Log
from memdriver.commiter import Commiter
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


class Driver(Doer):
    l: Log
    doers: list[Doer]
    flow_registry: FlowRegistry

    def __init__(self):
        self.l = Log()
        self.flow_registry = FlowRegistry()

        self.doers = [
            DefaultTransitDoer(),
            DefaultPauseDoer(),
            DefaultResumeDoer(),
            DefaultEndDoer(),
            DefaultNoopDoer(),
            DefaultSerializerDoer(),
            DefaultDeserializeDoer(),
            DefaultDereferenceDataDoer(),
            DefaultReferenceDataDoer(),
            DataLog(),
            FlowGetter(self.flow_registry),
            Commiter(self.l),
            Getter(self.l),
        ]

    def do(self, cmd: Command):
        for doer in self.doers:
            try:
                doer.do(cmd)
            except ErrCommandNotSupported as e:
                continue
            except Exception as e:
                raise Exception(f"{doer} do: {e}")

    def init(self, e: Engine):
        for doer in self.doers:
            try:
                doer.init(e)
            except Exception as e:
                raise Exception(f"{doer} init: {e}")

    def __enter__(self):
        with ExitStack() as stack:
            for doer in self.doers:
                stack.enter_context(doer)
            self._stack = stack.pop_all()

        return self

    def __exit__(self, typ, value, traceback):
        self._stack.__exit__(typ, value, traceback)
