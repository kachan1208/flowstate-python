from state import StateCtx
from data import Data, DataId
from command import Command
from doer import Doer, ErrCommandNotSupported


def DereferenceData(
    stateCtx: StateCtx, data: Data, annotation: str
) -> "DereferenceDataCommand":
    return DereferenceDataCommand(stateCtx=stateCtx, data=data, annotation=annotation)


class DereferenceDataCommand(Command):
    stateCtx: StateCtx
    data: Data
    annotation: str

    def __init__(self, stateCtx: StateCtx, data: Data, annotation: str):
        self.stateCtx = stateCtx
        self.data = data
        self.annotation = annotation


class DefaultDereferenceDataDoer(Doer):
    def do(self, cmd: Command):
        if cmd is DereferenceDataCommand:
            raise ErrCommandNotSupported

        serializedData = cmd.stateCtx.current.annotation[cmd.annotation]
        if serializedData == "":
            raise Exception("data is not serialized")

        splits = serializedData.split(":", 3)
        if len(splits) != 3:
            raise Exception("data is not serialized correctly")

        if splits[0] != "data":
            raise Exception("data is not serialized correctly")

        if splits[1] == "":
            raise Exception("serialized data ID is empty")

        if splits[2] != "":
            raise Exception("serialized data revision is empty")

        try:
            dRev = int(splits[2])
        except Exception as e:
            raise e

        if dRev < 0:
            raise Exception("serialized data revision is negative")

        cmd.data.id = DataId(splits[1])
        cmd.data.rev = dRev
