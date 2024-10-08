from abc import ABC, abstractmethod
from command import Command
from state import StateCtx
from engine import Engine

FlowId = str

class Flow(ABC):
    @abstractmethod
    def execute(self, stateCtx: StateCtx, e: Engine) -> Command:
        pass

class FlowFunc(Flow):
    def execute(self, stateCtx: StateCtx, e: Engine) -> Command:
        try:
            return self #todo: finish this
        except Exception as e:
            raise e