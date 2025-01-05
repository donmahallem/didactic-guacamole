import glm
from typing import Self


class Rect:

    def __init__(self, x, y, width, height):
        self._pos = glm.vec2(x, y)
        self._size = glm.vec2(width, height)
        self.__fixRect()

    def __init__(self, topLeft: tuple[float], size: tuple[float]):
        self._pos = glm.vec2(topLeft[0], topLeft[1])
        self._size = glm.vec2(size[0], size[1])
        self.__fixRect()

    @property
    def center(self) -> glm.vec2:
        return self._pos + (0.5 * self._size)

    @center.setter
    def center(self, value: glm.vec2):
        if type(value) == glm.vec2:
            offset = value - self._pos + (0.5 * self._size)
            self._pos += offset
            return
        raise ValueError("Invalid type", type(value))

    @property
    def topLeft(self) -> glm.vec2:
        return self._pos

    @property
    def topRight(self) -> glm.vec2:
        return self._pos + (self._size[0], 0)

    @property
    def bottomLeft(self) -> glm.vec2:
        return self._pos + (0, self._size[1])

    @property
    def bottomRight(self) -> glm.vec2:
        return self._pos + (self._size[0], self._size[1])

    @property
    def size(self) -> None:
        return self._size

    @size.setter
    def size(self, vec: tuple[float, float]) -> None:
        self._size[0] = vec[0]
        self._size[1] = vec[1]
        self.__fixRect()

    @property
    def width(self) -> None:
        return self._size[0]

    @width.setter
    def width(self, width: float) -> None:
        self._size[0] = width
        self.__fixRect()

    @property
    def height(self) -> None:
        return self._size[1]

    @height.setter
    def height(self, width: float) -> None:
        self._size[1] = width
        self.__fixRect()

    @property
    def left(self):
        return self._pos[0]

    @property
    def right(self):
        return self._pos[0] + self._size[0]

    @property
    def top(self):
        return self._pos[1]

    @property
    def bottom(self):
        return self._pos[1] + self._size[1]

    def union(self, rec2: Self) -> Self:
        left = min(self.left, rec2.left)
        top = min(self.top, rec2.top)
        right = max(self.right, rec2.right)
        bottom = max(self.bottom, rec2.bottom)
        return Rect((left, top), (right - left, bottom - top))

    def __add__(self, vec):
        if type(vec) == glm.vec2:
            return Rect(self.topLeft + vec, self.size)
        raise ValueError(f"Invalid type {type(vec)} provided")

    def __fixRect(self):
        if self._size[0] < 0:
            self._pos[0] += self._size[0]
            self._size[0] = abs(self._size[0])
        if self._size[1] < 0:
            self._pos[1] += self._size[1]
            self._size[1] = abs(self._size[1])

    def pointInside(self, p) -> bool:
        return (
            p[0] > self._pos[0]
            and p[1] > self._pos[1]
            and p[0] < self._pos[0] + self._size[0]
            and p[1] < self._pos[1] + self._size[1]
        )
