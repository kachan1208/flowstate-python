import logging
from doer import Doer
from state import StateCtx
from flow import Flow
from cmd_get_flow import GetFlow
from errors import ErrCommitConflict
from cmd_commit import CommitComand
from cmd_execute import ExecuteCommand
from cmd_resume import ResumeCommand
from cmd_transit import TransitCommand
from cmd_resume import ResumeCommand
from cmd_pause import PauseCommand
from cmd_delay import DelayCommand
from cmd_end import EndCommand
from cmd_noop import NoopCommand
from command import Command


ErrFlowNotFound = Exception("flow not found")


class Engine:
    def __init__(self, doer: Doer):
        self.d = doer

        try:
            doer.init(self)
        except Exception as e:
            raise Exception("driver init") from e

    def execute(self, stateCtx: StateCtx):
        stateCtx.e = self

        if stateCtx.current.id == "":
            raise Exception("state id is empty")

        while not stateCtx.done():
            if stateCtx.current.transition.toId == "":
                raise Exception("transition to id is empty")

            try:
                f = self.getFlow(stateCtx)
                cmd0 = f.execute(stateCtx, self)
                if cmd0 is ExecuteCommand:
                    cmd0.sync = True

                self.do(cmd0)
            except ErrCommitConflict as e:
                logging.info(f"engine: execute: {e}\n")
                return
            except Exception as e:
                raise e

            try:
                nextStateCtx = self.continueExecution(cmd0)
                if nextStateCtx is not None:
                    stateCtx = nextStateCtx
                    continue
            except Exception as e:
                raise e

    def do(self, *cmds: Command) -> None:
        if len(cmds) == 0:
            raise Exception("no commands to do")

        for cmd in cmds:
            try:
                self.__do(cmd)
            except Exception as e:
                raise e

    def __do(self, cmd0: Command) -> None:
        t = type(cmd0)
        if t == ExecuteCommand:
            if cmd0.sync:
                return

            # TODO: add asynio support
            try:
                self.execute(cmd0.stateCtx)
            except Exception as e:
                raise e

        else:
            try:
                return self.d.do(cmd0)
            except Exception as e:
                raise e

    def getFlow(self, stateCtx: StateCtx) -> Flow:
        cmd = GetFlow(stateCtx)
        try:
            self.d.do(cmd)
        except Exception as e:
            raise e

        return cmd.flow

    def continueExecution(self, cmd: Command) -> StateCtx | None:
        if cmd is CommitComand:
            if len(cmd.commands) != 1:
                raise Exception("commit command must have exactly one command")
            return self.continueExecution(cmd.commands[0])
        elif cmd is ExecuteCommand:
            return cmd.stateCtx
        elif cmd is TransitCommand:
            return cmd.stateCtx
        elif cmd is ResumeCommand:
            return cmd.stateCtx
        elif cmd is PauseCommand:
            return None
        elif cmd is DelayCommand:
            return None
        elif cmd is EndCommand:
            return None
        elif cmd is NoopCommand:
            return None
        else:
            raise Exception(f"unknown command 123: {type(cmd)}")
