DataId = str


class Data:
    def __init__(self, id: DataId = 0, rev: int = 0, b: bytearray = bytearray()):
        self.id = id
        self.rev = rev
        self.b = b

    def copy_to(self, to: "Data") -> "Data":
        to.id = self.id
        to.rev = self.rev
        to.b[:] = self.b

        return to

    def __copy__(self):
        return None

    def __deepcopy__(self, memodict):
        return None
