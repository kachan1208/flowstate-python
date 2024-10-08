from doer import Doer
from state import StateCtx
from flow import Flow
from cmd_get_flow import GetFlow

class Engine:
    def __init__(self, doer: Doer):
        self.d = doer

        try:
            doer.init(self)
        except Exception as e:
            raise Exception("driver init") from e
        
    def execute(stateCtx: StateCtx):
        stateCtx.e = self

        if stateCtx.current.id == '':
            raise Exception("state id is empty")
        
        while not stateCtx.done():
            if stateCtx.current.transition.toId == '' :
                raise Exception("transition to id is empty")

            try:
                f = self.getFlow(stateCtx)
            except Exception as e:
                raise e
            
            cmd0 = f.exe

    def getFlow(stateCtx: StateCtx) -> Flow:
        cmd = GetFlow(stateCtx)
        try:
            self.d.Do(cmd)
        except Exception as e:
            raise e
        
        return cmd.flow