from data import Data
from command import Command


def get_data(d: Data) -> "GetDataCommand":
    return GetDataCommand(d)


class GetDataCommand(Command):
    data: Data

    def __init__(self, d: Data):
        self.data = d

    def prepare(self):
        if self.data is None:
            raise Exception("data is None")

        if self.data.id == "":
            raise Exception("data id is empty")

        if self.data.rev < 0:
            raise Exception("data revision is negative")
