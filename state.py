from transition import Transition
from datetime import datetime
class State:
    def __init__(self) -> None:
        id: str = "" 
        rev: int = 0
        annotations: dict = {}
        labels: dict = {}
        commitedAtUnixMilli: int = 0
        transition: Transition = Transition()

    def setCommitedAt(self, commitedAt: datetime):
        self.commitedAtUnixMilli = round(commitedAt.now().timestamp() * 1000)

    def commitedAt(self) -> datetime:
        return datetime.fromtimestamp(self.commitedAtUnixMilli / 1000)
    
    def copyTo(self, to: 'State') -> 'State':
        to.id = self.id
        to.rev = self.rev
        to.annotations = self.annotations.copy()
        to.labels = self.labels.copy()
        to.commitedAtUnixMilli = self.commitedAtUnixMilli
        self.transition.CopyTo(to.transition)

        return to

    #def copyToCtx() TODO: impl

    def setAnnotation(self, name: str, value: str):
        self.annotations[name] = value

    def setLabel(self, name: str, value: str):
        self.labels[name] = value

    