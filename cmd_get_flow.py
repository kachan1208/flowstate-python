from command import Command
from state import StateCtx
from flow import Flow

class GetFlowCommand(Command):
    def __init__(self, stateCtx: StateCtx):
        self.stateCtx = stateCtx
        self.flow: Flow

    def cmd(self):
        pass

def GetFlow(stateCtx: StateCtx) -> GetFlowCommand:
    cmd = GetFlowCommand(stateCtx)
    return cmd
    
