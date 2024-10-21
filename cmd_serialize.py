import json
import base64

from state import StateCtx, State, StateAnnotation
from doer import Doer, ErrCommandNotSupported
from command import Command


def Serialize(
    serializableStateCtx: StateCtx, stateCtx: StateCtx, annotation: str
) -> "SerializeCommand":
    return SerializeCommand(serializableStateCtx, stateCtx, annotation)


class SerializeCommand(Command):
    def __init__(
        self, serializableStateCtx: StateCtx, stateCtx: StateCtx, annotation: str
    ):
        self.serializableStateCtx = serializableStateCtx
        self.stateCtx = stateCtx
        self.annotation = annotation


def DefaultSerializeDoer(Doer):
    def do(self, cmd: Command):
        if cmd is not SerializeCommand:
            raise ErrCommandNotSupported

        if cmd.annotation == "":
            raise Exception("store annotation name empty")

        if cmd.stateCtx.current.annotations[cmd.annotation] != "":
            raise Exception("store annotation already set")

        try:
            b = json.JSONEncoder().encode(cmd.serializableStateCtx)
        except Exception as e:
            raise e("json encode prev state ctx")

        serialized = base64.standard_b64encode(b)
        cmd.stateCtx.current.setAnnotation(cmd.annotation, serialized)
