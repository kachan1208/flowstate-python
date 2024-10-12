import logging
from doer import Doer
from state import StateCtx
from flow import Flow
from cmd_get_flow import GetFlow
from errors import ErrCommitConflict
from cmd_commit import CommitComand
from cmd_execute import ExecuteCommand

class Engine:
    def __init__(self, doer: Doer):
        self.d = doer

        try:
            doer.init(self)
        except Exception as e:
            raise Exception("driver init") from e
        
    def execute(self, stateCtx: StateCtx):
        stateCtx.e = self

        if stateCtx.current.id == '':
            raise Exception("state id is empty")
        
        while not stateCtx.done():
            if stateCtx.current.transition.toId == '' :
                raise Exception("transition to id is empty")

            try:
                f = self.getFlow(stateCtx)
                cmd0 = f.execute(stateCtx, self)
                e.do(cmd0)
            except ErrCommitConflict as e:
                logging.info(f"engine: execute: {e}\n")
                return
            except Exception as e:
                raise e
            
            try:
                stateCtx = self.continueExecution(cmd0)
            except Exception as e:
                raise e


    def getFlow(self, stateCtx: StateCtx) -> Flow:
        cmd = GetFlow(stateCtx)
        try:
            self.d.Do(cmd)
        except Exception as e:
            raise e 
        
        return cmd.flow
    
    def continueExecution(self, cmd: Command) -> StateCtx:
        t = type(cmd)
        if t == CommitComand:
            if len(cmd.commands) != 1:
                raise Exception("commit command must have exactly one command")
            return self.continueExecution(cmd.commands[0])
        elif t == ExecuteCommand:
            return cmd.stateCtx
        else:
            raise Exception(f"unknown command 123: {t}")