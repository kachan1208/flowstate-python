ErrCommandNotSupported = Exception("command not supported")


class Doer:
    def init(self, engine: "Engine") -> None:
        pass

    def do(self, cmd: "Command") -> None:
        pass

    def shutdown(self) -> None:
        pass
