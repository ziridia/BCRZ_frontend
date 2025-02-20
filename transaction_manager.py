
from abc import ABC, abstractmethod

# this is an abstract class that all other transaction managers should inherit from, and
# are expected to implement all methods of this class
class TransactionManager(ABC):
    
    # take the next input for the transaction and parse it accordingly
    @abstractmethod
    def next(self, user_input):
        pass

    # return true if the transaction is complete; false otherwise
    def isComplete(self):
        return self.state == -1

    # this should basically just keep track of the active user
    @abstractmethod
    def __init__(self, user):
        pass

    # should return a user object
    def getUser(self):
        return self.user