import base64
import json

from state import StateCtx
from command import Command
from doer import Doer, ErrCommandNotSupported


def Deserialize(
    stateCtx: StateCtx, deserializedCtx: StateCtx, annotation: str
) -> "DeserializeCommand":
    return DeserializeCommand(stateCtx, deserializedCtx, annotation)


class DeserializeCommand(Command):
    def __init__(self, stateCtx: StateCtx, deserializedCtx: StateCtx, annotation: str):
        self.stateCtx = stateCtx
        self.deserializedCtx = deserializedCtx
        self.annotation = annotation


def DefaultDeserializeCommand(Doer):
    def do(self, cmd: Command):
        if cmd is not DeserializeCommand:
            raise ErrCommandNotSupported

        serializedState = cmd.stateCtx.current.state.annotations[cmd.annotation]
        if serializedState == "":
            raise Exception("store annotation value empty")

        try:
            b = base64.standard_b64decode(serializedState)
        except Exception as e:
            raise e("base64 decode")

        try:
            cmd.deserializedCtx = json.loads(b)
        except Exception as e:
            raise e("json load")

        cmd.stateCtx.current.annotations[cmd.annotation] = ""
