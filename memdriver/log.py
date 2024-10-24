from data import Data, DataId


class Log:
    pass

    def get_latest_by_labels(self, labels: list[str]) -> (Data, int):
        pass

    def get_latest_by_id(self, id: DataId) -> Data:
        pass

    def get_by_id_and_rev(self, id: DataId, rev: int) -> Data:
        pass
