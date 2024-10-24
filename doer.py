ErrCommandNotSupported = Exception("command not supported")


class Doer:
    def init(self, engine) -> None:
        pass

    def do(self, cmd) -> None:
        pass

    def shutdown(self) -> None:
        pass
