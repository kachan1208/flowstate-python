from data import Data
from command import Command

def store_data(data: Data) -> "StoreDataCommand":
    return StoreDataCommand(data)

class StoreDataCommand(Command):
    def __init__(self, data: Data):
        self.data = data

    def prepare(self):
        if self.data is None:
            raise Exception("data is None")

        if self.data.id is None:
            raise Exception("data id is None")

        if len(self.data.b) == 0:
            raise Exception("data body is empty")