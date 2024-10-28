from state import StateCtx
from data import Data
from doer import Doer, ErrCommandNotSupported
from command import Command


def reference_data(
    state_ctx: StateCtx, data: Data, annotation: str
) -> "ReferenceDataCommand":
    return ReferenceDataCommand(state_ctx=state_ctx, data=data, annotation=annotation)


class ReferenceDataCommand(Command):
    state_ctx: StateCtx
    data: Data
    annotation: str

    def __init__(self, state_ctx: StateCtx, data: Data, annotation: str):
        self.state_ctx = state_ctx
        self.data = data
        self.annotation = annotation


class DefaultReferenceDataDoer(Doer):
    def do(self, cmd: Command):
        if not isinstance(cmd, ReferenceDataCommand):
            raise ErrCommandNotSupported

        if cmd.data.id == "":
            raise Exception("data id is empty")

        if cmd.data.rev < 0:
            raise Exception("data revision is negative")

        cmd.state_ctx.current.set_annotation(
            cmd.annotation, f"data:{cmd.data.id}:{cmd.data.rev}"
        )
