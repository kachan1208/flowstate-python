from doer import Doer

class Engine:
    def __init__(self, doer: Doer):
        self.doer = doer

        try:
            doer.init(self)
        except Exception as e:
            raise e
        
    def execute(state: State):
        print("Engine is running")