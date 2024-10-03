from flow import FlowId

class Transition:
    def __init__(self) -> None:
        fromId: FlowId = FlowId("")
        toId: FlowId = FlowId("")
        annotations: dict = {}

    def setAnnotation(self, name: str, value: str):
        self.annotations[name] = value

    def copyTo(self, to: 'Transition') -> 'Transition':
        to.fromId = self.fromId
        to.toId = self.toId
        to.annotations = self.annotations.copy()

        return to
    
    def string(self) -> str:
        return f"{self.fromId} -> {self.toId}"
        