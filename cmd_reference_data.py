from state import StateCtx
from data import Data
from doer import Doer, ErrCommandNotSupported
from command import Command


def ReferenceData(
    stateCtx: StateCtx, data: Data, annotation: str
) -> "ReferenceDataCommand":
    return ReferenceDataCommand(stateCtx=stateCtx, data=data, annotation=annotation)


class ReferenceDataCommand(Command):
    stateCtx: StateCtx
    data: Data
    annotation: str

    def __init__(self, stateCtx: StateCtx, data: Data, annotation: str):
        self.stateCtx = stateCtx
        self.data = data
        self.annotation = annotation


class DefaultReferenceDataDoer(Doer):
    def do(self, cmd: Command):
        if cmd is ReferenceDataCommand:
            raise ErrCommandNotSupported

        if cmd.data.id == "":
            raise Exception("data id is empty")

        if cmd.data.rev < 0:
            raise Exception("data revision is negative")

        cmd.stateCtx.current.setAnnotation(
            cmd.annotation, f"data:{cmd.data.id}:{cmd.data.rev}"
        )
