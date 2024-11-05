import asyncio

from cmd_watch import watch, WatchListener, WatchCommand
from command import Command
from doer import Doer, ErrCommandNotSupported
from engine import Engine
from state import State


class Recoverer(Doer):
    def __init__(self, failover_dur: int):
        self.failover_dur = failover_dur
        self.stopped_event = asyncio.Event()
        self.done_event = asyncio.Event()
        self.wl: WatchListener = None
        self.log: list[State] = []
        self.e: Engine = None

    def do(self, _: "Command"):
        raise ErrCommandNotSupported

    def init(self, engine: "Engine"):
        cmd: WatchCommand = watch()

        try:
            engine.do(cmd)
        except Exception as e:
            raise e

        self.wl = cmd.listener
        self.e = engine

    async def watch(self):
        try:
            while not self.done_event.is_set():
                await asyncio.sleep(1)
        finally:
            self.stopped_event.set()
