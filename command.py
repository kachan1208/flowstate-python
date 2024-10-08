from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def cmd(self):
        pass