import json
import base64

from state import StateCtx, State, StateAnnotation
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


class DefaultSerializeDoer(Doer):
    def do(self, cmd: Command):
        if cmd is not SerializeCommand:
            raise ErrCommandNotSupported

        if cmd.annotation == "":
            raise Exception("store annotation name empty")

        if cmd.state_ctx.current.annotations[cmd.annotation] != "":
            raise Exception("store annotation already set")

        try:
            b = json.JSONEncoder().encode(cmd.serializable_state_ctx)
        except Exception as e:
            raise e("json encode prev state ctx")

        serialized = base64.standard_b64encode(b)
        cmd.state_ctx.current.set_annotation(cmd.annotation, serialized)
