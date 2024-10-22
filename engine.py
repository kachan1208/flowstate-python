import logging
from doer import Doer
from state import StateCtx
from flow import Flow
from cmd_get_flow import get_flow
from errors import ErrCommitConflict
from cmd_commit import CommitCommand
from cmd_execute import ExecuteCommand
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

    def execute(self, state_ctx: StateCtx):
        state_ctx.e = self

        if state_ctx.current.id == "":
            raise Exception("state id is empty")

        while not state_ctx.done():
            if state_ctx.current.transition.to_id == "":
                raise Exception("transition to id is empty")

            try:
                f = self.get_flow(state_ctx)
                cmd0 = f.execute(state_ctx, self)
                if cmd0 is ExecuteCommand:
                    cmd0.sync = True

                self.do(cmd0)
            except ErrCommitConflict as e:
                logging.info(f"engine: execute: {e}\n")
                return
            except Exception as e:
                raise e

            try:
                nextStateCtx = self.continue_execution(cmd0)
                if nextStateCtx is not None:
                    state_ctx = nextStateCtx
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
                self.execute(cmd0.state_ctx)
            except Exception as e:
                raise e

        else:
            try:
                return self.d.do(cmd0)
            except Exception as e:
                raise e

    def get_flow(self, state_ctx: StateCtx) -> Flow:
        cmd = get_flow(state_ctx)
        try:
            self.d.do(cmd)
        except Exception as e:
            raise e

        return cmd.flow

    def continue_execution(self, cmd: Command) -> StateCtx | None:
        typ = type(cmd)
        if typ is CommitCommand:
            if len(cmd.commands) != 1:
                raise Exception("commit command must have exactly one command")
            return self.continue_execution(cmd.commands[0])
        elif typ is ExecuteCommand:
            return cmd.state_ctx
        elif typ is TransitCommand:
            return cmd.state_ctx
        elif typ is ResumeCommand:
            return cmd.state_ctx
        elif typ is PauseCommand:
            return None
        elif typ is DelayCommand:
            return None
        elif typ is EndCommand:
            return None
        elif typ is NoopCommand:
            return None
        else:
            raise Exception(f"unknown command 123: {type(cmd)}")
