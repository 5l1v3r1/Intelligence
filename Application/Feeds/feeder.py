from abc import ABC, abstractmethod


description = """
    Baseclass for all  feed modules

"""

class Feeder(ABC):


    def __init__(self, type, name,by):
        self.name = name
        self.type=type
        self.by=by


    @abstractmethod
    def checkstatus(self):
        pass

