import time
from cmd_resume import resumed
from state import StateCtx
from cmd_pause import paused
import asyncio


def track(state_ctx: StateCtx, trkr: "Tracker"):
    postfix = ""
    if trkr.include_state:
        if resumed(state_ctx.current):
            postfix = ":resumed"
        elif paused(state_ctx.current):
            postfix = ":paused"

    if trkr.include_task_id:
        postfix += f"{postfix}:{state_ctx.current.id}"

    trkr.visited.append(f"{state_ctx.current.transition.to_id}{postfix}")


class Tracker:
    def __init__(self, include_task_id: bool = False, include_state: bool = False):
        self.include_task_id = include_task_id
        self.include_state = include_state
        self.visited: list[str] = []

    def get_visited(self) -> list[str]:
        return self.visited[:]

    def visited_sorted(self) -> list[str]:
        return sorted(self.visited)

    def wait_sorted_visited_equal(
        self,
        exp_visited: list[str],
        wait: int,
    ) -> list[str]:
        visited: list[str]

        def condition():
            nonlocal visited
            visited = self.visited_sorted()
            return visited == exp_visited

        assert_eventually(func=condition, timeout=wait, interval=0.05)

        assert exp_visited == self.visited
        return self.visited

    async def wait_visited_equal(
        self,
        exp_visited: list[str],
        wait: int,
    ) -> list[str]:
        visited: list[str] = []

        def condition():
            nonlocal visited
            visited = self.visited[:]
            return visited == exp_visited

        await assert_eventually(func=condition, timeout=wait, interval=0.05)

        assert exp_visited == visited
        return visited


async def assert_eventually(func, timeout=1, interval=0.1):
    end_time = time.time() + timeout
    while end_time > time.time():
        if func():
            return

        await asyncio.sleep(interval)

    raise AssertionError("condition not met within timeout")
