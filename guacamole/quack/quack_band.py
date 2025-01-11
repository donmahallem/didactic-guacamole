from .quack_obstacle import QuackObstacle
from enum import Enum


class QuackBandType(Enum):
    SAFE = 1
    WATER = 2
    STREET = 3
    START = 4
    END = 5


class QuackBand:
    def __init__(
        self,
        id: int,
        type: QuackBandType,
        initialOffset: float,
        obstacles: list[QuackObstacle] = None,
    ):
        self._id = id
        self._type = type
        self._initialOffset = initialOffset
        self._obstacles = obstacles

    @property
    def obstacles(self) -> list[QuackObstacle]:
        return self._obstacles

    @property
    def id(self) -> int:
        return self._id

    @property
    def type(self) -> QuackBandType:
        return self._type

    @property
    def initalOffset(self) -> float:
        return self._initialOffset

    def __repr__(self):
        return (
            f'Quackband{{id:"{self._id}",type:"{self._type}",initialOffset:"{self._initialOffset}",'
            + f"obstacles:[{len(self._obstacles) if self._obstacles else 0}]}}"
        )

    def __eq__(self, value):
        return (
            self._id == value.id
            and self._type == value.type
            and self._initialOffset == value.initalOffset
            and self._obstacles == value._obstacles
        )
