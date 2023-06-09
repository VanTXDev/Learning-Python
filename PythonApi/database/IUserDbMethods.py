from abc import ABC, abstractmethod

class IUserDbMethods(ABC):

    @abstractmethod
    def __init__(self, db):
        pass
    
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def login (self, username, password):
        pass