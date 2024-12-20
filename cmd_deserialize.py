import base64
import json

from state import StateCtx
from command import Command
from doer import Doer, ErrCommandNotSupported


def deserialize(
    state_ctx: StateCtx, deserialized_ctx: StateCtx, annotation: str
) -> "DeserializeCommand":
    return DeserializeCommand(state_ctx, deserialized_ctx, annotation)


class DeserializeCommand(Command):
    def __init__(
        self, state_ctx: StateCtx, deserialized_ctx: StateCtx, annotation: str
    ):
        self.state_ctx = state_ctx
        self.deserialized_ctx = deserialized_ctx
        self.annotation = annotation


class DefaultDeserializeDoer(Doer):
    async def do(self, cmd: Command):
        if not isinstance(cmd, DeserializeCommand):
            raise ErrCommandNotSupported

        serialized_state = cmd.state_ctx.current.annotations.get(cmd.annotation)
        if serialized_state is None or serialized_state is "":
            raise Exception("store annotation value empty")

        try:
            b = base64.standard_b64decode(serialized_state)
        except Exception as e:
            raise e("base64 decode")

        try:
            data = json.loads(b)
            cmd.deserialized_ctx.from_dict(data)
        except Exception as e:
            raise e("json load")

        cmd.state_ctx.current.annotations[cmd.annotation] = ""
