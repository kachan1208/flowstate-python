import asyncio
from asyncio.queues import Queue

from cmd_commit import commit_state_ctx, commit
from engine import Engine
from doer import Doer, ErrCommandNotSupported
from command import Command
from cmd_delay import DelayCommand, DelayCommitAnnotation
from errors import ErrCommitConflict


class Delayer(Doer):
    def __init__(self):
        self.done_event: asyncio.Event = asyncio.Event()
        self.e: Engine | None = None

    async def do(self, cmd: Command):
        if not isinstance(cmd, DelayCommand):
            raise ErrCommandNotSupported

        asyncio.create_task(self.__do(cmd))

    async def __do(self, cmd: DelayCommand):
        try:
            cmd.prepare()
            ticks, ticks_stop = ticker(cmd.duration)
            while await ticks.get():
                if (
                    cmd.delay_state_ctx.current.transition.annotations[
                        DelayCommitAnnotation
                    ]
                    == "True"
                ):
                    await self.e.do(commit(commit_state_ctx(cmd.delay_state_ctx)))
                    await self.e.execute(cmd.delay_state_ctx)

            ticks_stop.set()
        except Exception as e:
            raise Exception(f"ERROR: memdriver: delayer: engine: %{e}")

    def init(self, e: Engine):
        self.e = e

    def shutdown(self):
        self.done_event.set()


def ticker(delay: float):
    q = Queue(maxsize=1)
    c = asyncio.Event()

    async def tick():
        t: int = 0
        while not c.is_set():
            t += delay
            await asyncio.sleep(delay)
            if not q.full():
                await q.put(t)

    asyncio.create_task(tick())
    return q, c
