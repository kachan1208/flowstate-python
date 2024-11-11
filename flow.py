from typing import Any, Callable, Coroutine
from command import Command

FlowId = str


class Flow:
    async def execute(self, state_ctx: "StateCtx", e: "Engine") -> Command:
        pass


class FlowFunc(Flow):
    def __init__(self, func):
        self.func = func

    async def execute(self, state_ctx: "StateCtx", e: "Engine") -> "Command":
        return await self.func(state_ctx, e)
