from abc import ABC, abstractmethod


class DatabaseDriverBase(ABC):
    """
    Force implementation of some methods in the event a new driver is
    added to the database package.
    """

    @abstractmethod
    async def upsert(self, entity, states):
        pass

    @abstractmethod
    async def get(self, entity, state):
        pass

    @abstractmethod
    async def increment(self, entity, state, value):
        pass
