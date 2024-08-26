class State:
    def __init__(self) -> None:
        id: str = "" 
        rev: int = 0
        annotations: dict = {}
        labels: dict = {}
        commitedAt: int = 0
        transition: str = "" #TODO: impl

    def setCommitedAt(self, commitedAt: int):
        self.commitedAt = commitedAt

    def commitedAt(self) -> int:
        return self.commitedAt
    
    def copyTo(self, to: State) -> State:
        to.id = self.id
        to.rev = self.rev
        to.annotations = self.annotations
        to.labels = self.labels
        to.commitedAt = self.commitedAt
        to.transition = self.transition

        return to

    #def copyToCtx() TODO: impl

    def setAnnotation(self, name: str, value: str):
        self.annotations[name] = value

    def setLabel(self, name: str, value: str):
        self.labels[name] = value

    