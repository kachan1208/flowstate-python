import pickle
import base64

from state import StateCtx, State
from doer import Doer, ErrCommandNotSupported
from command import Command


def serialize(
    serializable_state_ctx: StateCtx, state_ctx: StateCtx, annotation: str
) -> "SerializeCommand":
    return SerializeCommand(serializable_state_ctx, state_ctx, annotation)


class SerializeCommand(Command):
    def __init__(
        self, serializable_state_ctx: StateCtx, state_ctx: StateCtx, annotation: str
    ):
        self.serializable_state_ctx = serializable_state_ctx
        self.state_ctx = state_ctx
        self.annotation = annotation


class DefaultSerializerDoer(Doer):
    async def do(self, cmd: Command):
        if not isinstance(cmd, SerializeCommand):
            raise ErrCommandNotSupported

        if cmd.annotation == "":
            raise Exception("store annotation name empty")

        if cmd.state_ctx.current.annotations.get(cmd.annotation) is not None:
            raise Exception("store annotation already set")

        try:
            b = cmd.serializable_state_ctx.to_json()
        except Exception as e:
            raise e("json encode prev state ctx")

        serialized = base64.standard_b64encode(b)
        cmd.state_ctx.current.set_annotation(cmd.annotation, serialized)
