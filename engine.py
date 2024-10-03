from doer import Doer
from state import State

class Engine:
    def __init__(self, doer: Doer):
        self.doer = doer

        try:
            doer.init(self)
        except Exception as e:
            raise e
        
    def execute(state: State):
        print("Engine is running")