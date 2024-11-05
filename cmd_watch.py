from asyncio.queues import Queue
from command import Command
from engine import Engine


class WatchListener:
    def listen(self) -> Queue:
        pass

    def close(self):
        pass


def watch(labels: dict[str, str] = None) -> "WatchCommand":
    return WatchCommand().with_or_labels(labels)


def do_watch(e: "Engine", cmd: "WatchCommand") -> "WatchListener":
    e.do(cmd)

    return cmd.listener


class WatchCommand(Command):
    def __init__(
        self,
        since_rev: int = 0,
        since_latest: bool = False,
        since_time: int = 0,
        labels: list[dict[str, str]] = None,
        watch_listener: WatchListener = None,
    ):
        self.since_rev: int = since_rev
        self.since_latest: bool = since_latest
        self.since_time: int = since_time
        if labels is None:
            self.labels: list[dict[str, str]] = []

        self.listener: WatchListener = watch_listener

    def with_since_rev(self, rev: int) -> "WatchCommand":
        self.since_latest = False
        self.since_rev = rev
        return self

    def with_since_latest(self) -> "WatchCommand":
        self.since_latest = True
        self.since_rev = 0
        return self

    def with_since_time(self, time: int) -> "WatchCommand":
        self.since_time = time
        return self

    def with_or_labels(self, labels: dict[str, str]) -> "WatchCommand":
        if labels is None or len(labels) == 0:
            return self

        self.labels.append(labels)
        return self
