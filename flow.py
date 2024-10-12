from abc import ABC, abstractmethod
from command import Command
from state import StateCtx
from engine import Engine

FlowId = str

class Flow(ABC):
    @abstractmethod
    def execute(self, stateCtx: StateCtx, e: Engine) -> Command:
        pass

def FlowFunc(func):
    def execute(self, stateCtx: StateCtx, e: Engine) -> Command:
        return func(self, stateCtx, e)
    return execute