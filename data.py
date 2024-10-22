DataId = str


class Data:
    id: DataId
    rev: int
    b: bytearray

    def __init__(self, id: DataId, rev: int, b: bytearray):
        self.id = id
        self.rev = rev
        self.b = b

    def copyTo(self, to: "Data") -> "Data":
        to.id = self.id
        to.rev = self.rev
        to.b[:] = self.b

        return to

    def __copy__(self):
        return None

    def __deepcopy__(self, memodict={}):
        return None
