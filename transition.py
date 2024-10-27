from flow import FlowId


class Transition:
    from_id: FlowId
    to_id: FlowId
    annotations: dict

    def __init__(
        self, from_id: "FlowId" = "", to_id: "FlowId" = "", annotations: dict = {}
    ) -> None:
        self.from_id = from_id
        self.to_id = to_id
        self.annotations = annotations

    def set_annotation(self, name: str, value: str):
        self.annotations[name] = value

    def copy_to(self, to: "Transition") -> "Transition":
        to.from_id = self.from_id
        to.to_id = self.to_id
        to.annotations = self.annotations.copy()

        return to

    def string(self) -> str:
        return f"{self.from_id} -> {self.to_id}"
