from enum import Enum


class QuackObstacleType(Enum):
    CAR = 0
    TURTLE = 3
    LOG = 4


class QuackObstacle:
    def __init__(self, type, pos, size):
        self._type = type
        self._pos = pos
        self._size = size

    @property
    def type(self):
        return self._type

    @property
    def position(self):
        return self._pos

    @property
    def size(self):
        return self._size

    def __eq__(self, value):
        if value:
            return (
                self._type == value.type
                and self._pos == value.position
                and self._size == value.size
            )
        return False

    def __repr__(self):
        return f"QuackObstacle{{position:{self.position},type:{self.type},size:{self.size}}}"
