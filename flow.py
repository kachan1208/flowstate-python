from command import Command


FlowId = str


class Flow:
    def execute(self, state_ctx, e) -> Command:
        pass


class FlowFunc(Flow):
    def __init__(self, func):
        self.func = func

    def execute(self, state_ctx, e) -> Command:
        return self.func(state_ctx, e)
