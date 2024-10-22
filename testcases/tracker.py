import time


class Tracker:
    include_task_id: bool
    include_state: bool
    visited: list[str]

    def visited(self) -> list[str]:
        return self.visited[:]

    def visited_sorted(self) -> list[str]:
        return sorted(self.visited)

    def wait_sorted_visited_equal(
        self,
        expVisited: list[str],
        wait: int,
    ) -> list[str]:
        visited: list[str]

        def condition():
            nonlocal visited
            visited = self.visited_sorted()
            return visited == expVisited

        assert_eventually(func=condition, timeout=wait, interval=0.05)

        assert expVisited == visited
        return visited

    def wait_visited_equal(
        self,
        expVisited: list[str],
        wait: int,
    ) -> list[str]:
        visited: list[str]

        def condition():
            nonlocal visited
            visited = self.visited()
            return visited == expVisited

        assert_eventually(func=condition, timeout=wait, interval=0.05)

        assert expVisited == visited
        return visited


def assert_eventually(func, timeout=1, interval=0.1):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if func():
            return

        time.sleep(interval)

    raise AssertionError("condition not met within timeout")