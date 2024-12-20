import asyncio
import logging
from contextlib import ExitStack

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
        self.d: Doer = doer
        self.done: asyncio.Event = asyncio.Event()

        try:
            doer.init(self)
        except Exception as e:
            raise Exception("driver init") from e

    async def execute(self, state_ctx: StateCtx):
        state_ctx.e = self

        if state_ctx.current.id == "":
            raise Exception("state id is empty")

        while not self.done.is_set():
            if state_ctx.current.transition.to_id == "":
                raise Exception("transition to id is empty")

            try:
                f = await self.get_flow(state_ctx)
                cmd = await f.execute(state_ctx, self)
                if isinstance(cmd, ExecuteCommand):
                    cmd.sync = True

                await self.do(cmd)
            except ErrCommitConflict as e:
                logging.info(f"engine: execute: {e}\n")
                return
            except Exception as e:
                raise e

            try:
                next_state_ctx = self.continue_execution(cmd)
                if next_state_ctx is not None:
                    state_ctx = next_state_ctx
                    continue
            except Exception as e:
                raise e

            return

    async def do(self, *cmds: Command) -> None:
        if len(cmds) == 0:
            raise Exception("no commands to do")

        for cmd in cmds:
            try:
                await self.__do(cmd)
            except Exception as e:
                raise e

    async def __do(self, cmd: Command) -> None:
        if isinstance(cmd, ExecuteCommand):
            if cmd.sync:
                return

            async def exec():
                try:
                    await self.execute(cmd.state_ctx)
                except Exception as e:
                    logging.error(f"engine: go execute: {e}\n")

            asyncio.create_task(exec())

        else:
            try:
                return await self.d.do(cmd)
            except Exception as e:
                raise e

    async def get_flow(self, state_ctx: StateCtx) -> Flow:
        cmd = get_flow(state_ctx)
        try:
            await self.d.do(cmd)
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
            raise Exception(f"unknown command: {typ}")

    def __enter__(self):
        with ExitStack() as stack:
            stack.enter_context(self.d)
            self._stack = stack.pop_all()

        return self

    def __exit__(self, typ, value, traceback):
        self.done.set()
        self._stack.__exit__(typ, value, traceback)
