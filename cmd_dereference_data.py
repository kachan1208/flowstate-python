from state import StateCtx
from data import Data, DataId
from command import Command
from doer import Doer, ErrCommandNotSupported


def dereference_data(
    state_ctx: StateCtx, data: Data, annotation: str
) -> "DereferenceDataCommand":
    return DereferenceDataCommand(state_ctx, data, annotation)


class DereferenceDataCommand(Command):
    def __init__(self, state_ctx: StateCtx, data: Data, annotation: str):
        self.state_ctx: StateCtx = state_ctx
        self.data: Data = data
        self.annotation: str = annotation


class DefaultDereferenceDataDoer(Doer):
    async def do(self, cmd: Command):
        if not isinstance(cmd, DereferenceDataCommand):
            raise ErrCommandNotSupported

        serialized_data = cmd.state_ctx.current.annotations[cmd.annotation]
        if serialized_data == "":
            raise Exception("data is not serialized")

        splits = serialized_data.split(":", 3)
        if len(splits) != 3:
            raise Exception("data is not serialized correctly")

        if splits[0] != "data":
            raise Exception("data is not serialized correctly")

        if splits[1] == "":
            raise Exception("serialized data ID is empty")

        if splits[2] == "":
            raise Exception("serialized data revision is empty")

        try:
            d_rev = int(splits[2])
        except Exception as e:
            raise e

        if d_rev < 0:
            raise Exception("serialized data revision is negative")

        cmd.data.id = DataId(splits[1])
        cmd.data.rev = d_rev
