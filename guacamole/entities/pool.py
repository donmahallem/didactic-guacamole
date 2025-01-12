from typing import Dict, Generic, TypeVar

T = TypeVar("T")


class Pool(Generic[T]):
    def __init__(self):
        self._pool: list[T] = []

    def createItem(self) -> T:
        raise NotImplementedError()

    def returnItem(self, item: T):
        if item in self._pool:
            raise ValueError("The item is already in the pool")
        self._pool.append(item)

    def getItem(self) -> T:
        if len(self._pool) == 0:
            return self.createItem()
        return self._pool.pop(0)
