import asyncio
from engine import Engine
from doer import Doer, ErrCommandNotSupported
from command import Command
from cmd_delay import DelayCommand


class Delayer(Doer):
    def __init__(self):
        self.done_event: asyncio.Event = asyncio.Event()
        self.e: Engine

    def do(self, cmd: Command):
        if not isinstance(cmd, DelayCommand):
            raise ErrCommandNotSupported

        try:
            cmd.prepare()
        except Exception as e:
            raise e
