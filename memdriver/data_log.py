from cmd_store_data import StoreDataCommand
from cmd_get_data import GetDataCommand
from data import Data, DataId
from command import Command
from doer import Doer, ErrCommandNotSupported


class DataLog(Doer):
    def __init__(self):
        self.entries = []
        self.rev = 0

    def do(self, cmd: Command):
        typ = type(cmd)
        if typ is StoreDataCommand:
            return self._do_store(cmd)
        elif typ is GetDataCommand:
            return self._do_get(cmd)

        return ErrCommandNotSupported

    def append(self, data: Data):
        self.rev += 1
        data.rev = self.rev
        self.entries.append(data.copy_to(Data()))

    def get(self, id: DataId, rev: int) -> Data:
        for e in self.entries:
            if e.id == id and e.rev == rev:
                return e

        raise Exception("data not found")

    def _do_get(self, cmd: GetDataCommand):
        try:
            cmd.prepare()
        except Exception as e:
            raise e

        data = self.get(cmd.data.id, cmd.data.rev)
        data.copy_to(cmd.data)

    def _do_store(self, cmd: StoreDataCommand):
        try:
            cmd.prepare()
        except Exception as e:
            raise e

        self.append(cmd.data)
