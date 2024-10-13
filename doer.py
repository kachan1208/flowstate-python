from engine import Engine
from command import Command


ErrCommandNotSupported = Exception("command not supported")


class Doer:
    def init(self, engine: Engine) -> None:
        pass

    def do(self, cmd: Command) -> None:
        pass

    def shutdown(self) -> None:
        pass


# TODO: rework once get used to decorators and understand the analogue in
# python. go uses http.HandlerFunc as decoratorin this case we have
# a DoerFunc type alias and few methods adds to it, but it's not implemented
def DoerFunc(func):
    def do(self, cmd: Command) -> None:
        return func(self, cmd)

    return do
