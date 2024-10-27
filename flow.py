FlowId = str


class Flow:
    def execute(self, state_ctx: "StateCtx", e: "Engine") -> "Command":
        pass


class FlowFunc(Flow):
    def __init__(self, func):
        self.func = func

    def execute(self, state_ctx: "StateCtx", e: "Engine") -> "Command":
        return self.func(state_ctx, e)
