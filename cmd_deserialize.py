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
    def do(self, cmd: Command):
        if cmd is not DeserializeCommand:
            raise ErrCommandNotSupported

        serializedState = cmd.state_ctx.current.state.annotations[cmd.annotation]
        if serializedState == "":
            raise Exception("store annotation value empty")

        try:
            b = base64.standard_b64decode(serializedState)
        except Exception as e:
            raise e("base64 decode")

        try:
            cmd.deserialized_ctx = json.loads(b)
        except Exception as e:
            raise e("json load")

        cmd.state_ctx.current.annotations[cmd.annotation] = ""
