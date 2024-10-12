from state import StateCtx
from command import Command

class ExecuteCommand(Command):
    def __init__(self, stateCtx: StateCtx):
        self.sync: bool
        self.stateCtx = stateCtx

def Execute(stateCtx: StateCtx) -> ExecuteCommand:
    return ExecuteCommand(stateCtx)
