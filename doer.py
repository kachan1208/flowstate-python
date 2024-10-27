class ErrCommandNotSupported(Exception):
    def __init__(self, msg="Error command not supported", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class Doer:
    def init(self, engine: "Engine") -> None:
        pass

    def do(self, cmd: "Command") -> None:
        pass

    def __enter__(self):
        pass

    def __exit__(self, typ, value, tracebacks):
        pass
