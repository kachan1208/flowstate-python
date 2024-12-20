from datetime import datetime
from idlelib.pyparse import trans

from flow import FlowFunc
from memdriver.driver import Driver
from testcases.tracker import Tracker, track
from state import State, StateCtx
from engine import Engine
from command import Command
from cmd_commit import commit
from cmd_pause import pause
from cmd_delay import delay
from cmd_transit import transit
from cmd_end import end
from cmd_noop import noop
import croniter
import time


import pytest


@pytest.mark.asyncio
async def test_cron():
    driver = Driver()
    flow_registry = driver.flow_registry

    tracker = Tracker()

    async def cron_flow(cron_state_ctx: StateCtx, e: Engine) -> "Command":
        track(cron_state_ctx, tracker)

        now = round(time.time())
        try:
            cron = croniter.croniter(cron_state_ctx.current.annotations["cron"])
        except Exception as e:
            cron_state_ctx.current.set_annotation("error", str(e))
            return commit(end(cron_state_ctx))

        if cron.get_next(start_time=time.time()) == 0:
            cron_state_ctx.current.set_annotation("error", "cron time is 0")
            return commit(end(cron_state_ctx))

        task_flow_id = cron_state_ctx.current.annotations["task"]
        if task_flow_id == "":
            cron_state_ctx.current.set_annotation("error", "task flow id is empty")
            return commit(end(cron_state_ctx))

        next_times = [cron.next(start_time=now), cron.next(start_time=now + 1)]
        if now < next_times[0] <= now + 1:
            task_state_ctx = StateCtx(
                current=State(
                    id=f"task_{int(next_times[0])}",
                    annotations={
                        "cron": cron_state_ctx.current.annotations["cron"],
                        "cron_task": "True",
                    },
                ),
            )

            try:
                await e.do(
                    commit(
                        pause(cron_state_ctx),
                        delay(cron_state_ctx, next_times[1] - now),
                        transit(task_state_ctx, task_flow_id),
                    ),
                )
            except Exception as e:
                raise e

            return noop(cron_state_ctx)

        try:
            await e.do(
                commit(
                    pause(cron_state_ctx),
                    delay(cron_state_ctx, next_times[0] - time.time()),
                )
            )
        except Exception as e:
            raise e

        return noop(cron_state_ctx)

    flow_registry.set_flow("cron", FlowFunc(cron_flow))

    async def task(state_ctx: StateCtx, _: Engine) -> "Command":
        track(state_ctx, tracker)

        return commit(end(state_ctx))

    flow_registry.set_flow("task", FlowFunc(task))

    with Engine(driver) as e:
        state_ctx: StateCtx = StateCtx(
            current=State(
                id="cron",
                annotations={
                    "cron": "* * * * * * *",
                    "task": "task",
                },
            ),
        )

        await e.do(commit(transit(state_ctx, "cron")))
        await e.execute(state_ctx)

    assert tracker.visited == ["cron", "task", "cron", "task", "cron", "task"]
