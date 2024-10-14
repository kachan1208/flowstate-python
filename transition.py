from flow import FlowId


class Transition:
    fromId: FlowId
    toId: FlowId
    annotations: dict

    def __init__(self, frowId: FlowId, toId: FlowId, annotations: dict) -> None:
        self.fromId = frowId
        self.toId = toId
        self.annotations = annotations

    def setAnnotation(self, name: str, value: str):
        self.annotations[name] = value

    def copyTo(self, to: "Transition") -> "Transition":
        to.fromId = self.fromId
        to.toId = self.toId
        to.annotations = self.annotations.copy()

        return to

    def string(self) -> str:
        return f"{self.fromId} -> {self.toId}"
