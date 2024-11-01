from cmd_commit import CommitStateCtxCommand, CommitCommand, CommittableCommand
from cmd_execute import ExecuteCommand
from errors import ErrCommitConflict
from memdriver.log import Log
from doer import Doer, ErrCommandNotSupported
from command import Command
from engine import Engine


class Commiter(Doer):
    def __init__(self, l: Log):
        self.l: Log = l
        self.e: Engine = None

    def do(self, cmd: Command):
        if isinstance(cmd, CommitStateCtxCommand):
            return

        if not isinstance(cmd, CommitCommand):
            raise ErrCommandNotSupported

        if len(cmd.commands) == 0:
            raise Exception("no commands to commit")

        with self.l:
            for c in cmd.commands:
                if isinstance(c, CommitCommand):
                    raise Exception("commit command not allowed inside another commit")

                if isinstance(c, ExecuteCommand):
                    raise Exception("execute command not allowed inside commit")

                try:
                    self.e.d.do(c)
                except Exception as e:
                    raise e

                if not isinstance(c, CommittableCommand):
                    continue

                state_ctx = c.committable_state_ctx()
                if state_ctx.current.id == "":
                    raise Exception("state id is empty")

                _, rev = self.l.get_latest_by_id(state_ctx.current.id)
                if rev != state_ctx.commited.rev:
                    raise ErrCommitConflict

                self.l.append(state_ctx)

            try:
                self.l.commit()
            except Exception as e:
                self.l.rollback()
                raise e

    def init(self, e: "Engine"):
        self.e: Engine = e
        return
