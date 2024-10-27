from cmd_get import GetCommand
from memdriver.log import Log
from doer import Doer, ErrCommandNotSupported
from command import Command


class Getter(Doer):
    def __init__(self, log: Log):
        self.l = log

    def do(self, cmd: Command):
        if not isinstance(cmd, GetCommand:
            return ErrCommandNotSupported

        if len(cmd.labels) > 0:
            state_ctx, _ = self.l.get_latest_by_labels(cmd.labels)
            if state_ctx is None:
                raise Exception(f"state not found by labels {cmd.labels}")
            state_ctx.copy_to(cmd.state_ctx)
        elif cmd.id != "" and cmd.rev == 0:
            state_ctx, _ = self.l.get_latest_by_id(cmd.id)
            if state_ctx is None:
                raise Exception(f"state not found by id {cmd.id}")
            state_ctx.copy_to(cmd.state_ctx)
        elif cmd.id != "" and cmd.rev > 0:
            state_ctx, _ = self.l.get_by_id_and_rev(cmd.id, cmd.rev)
            if state_ctx is None:
                raise Exception(f"state not found by id {cmd.id} and rev {cmd.rev}")
            state_ctx.copy_to(cmd.state_ctx)
        else:
            raise Exception("invalid get command")
