import random
import numpy as np


class DotsGame:

    def __init__(self, colors=3, size=(28, 14)):
        self._size = size
        self.colors = colors
        self.reset()

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, f) -> None:
        self._field = np.array(f, dtype=np.uint8)
        self._size = self._field.shape

    @property
    def seed(self):
        return self._seed

    @property
    def colors(self) -> None:
        return self._colors

    @colors.setter
    def colors(self, val) -> None:
        if val <= 0 or not (isinstance(val, int) and val.is_integer()):
            raise ValueError(f"Colors is supposed to be an integer greater than 0")
        self._colors = int(val)

    @property
    def score(self) -> int:
        return self._score

    def reset(self, seed=random.randbytes(1024)):
        # abs as seed must be non-negative
        self._seed = abs(hash(seed))
        rnd = np.random.default_rng(self._seed)
        self._field = rnd.integers(1, self._colors + 1, self._size, dtype=np.uint8)
        self._score = 0

    def selectConnected(self, y, x):
        if isinstance(y, tuple) and len(y) >= 2:
            selectedY, selectedX = y
        else:
            selectedY, selectedX = y, x
        lookingFor = self._field[selectedY, selectedX]
        if lookingFor <= 0:
            return None
        selected = list([(selectedY, selectedX)])
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        checkIdx = 0
        while True:
            if checkIdx >= len(selected):
                break
            checkCurrent = selected[checkIdx]
            for dir in dirs:
                nextPos = (checkCurrent[0] + dir[0], checkCurrent[1] + dir[1])
                if (
                    nextPos[0] < 0
                    or nextPos[1] < 0
                    or nextPos[0] >= self._size[0]
                    or nextPos[1] >= self._size[1]
                ):
                    continue
                if (
                    self._field[nextPos[0], nextPos[1]] == lookingFor
                    and nextPos not in selected
                ):
                    selected.append(nextPos)
            checkIdx += 1
        self._score += len(selected) * (len(selected) - 1)
        return selected

    def selectDots(self, dots):
        selected = dots if isinstance(dots, list) else self.selectConnected(dots)
        if selected is None:
            return
        minX = self._size[1] + 1
        maxX = -1
        for dot in selected:
            self._field[dot[0], dot[1]] = 0
            minX = min(minX, dot[1])
            maxX = max(maxX, dot[1])
        return len(selected), self.applyGravity(minX, maxX)

    def applyGravity(self, l=None, r=None):
        left = l if l else 0
        right = r if r else self._size[1] - 1
        moved = set()
        for x in range(left, right + 1):
            lastEmptyY = -1
            for y in range(self._size[0]):
                if self._field[y, x] == 0 and lastEmptyY < 0:
                    lastEmptyY = y
                    continue
                elif self._field[y, x] != 0 and lastEmptyY >= 0:
                    moved.add(((y, x), (lastEmptyY, x), int(self._field[y, x])))
                    self._field[lastEmptyY, x] = self._field[y, x]
                    self._field[y, x] = 0
                    lastEmptyY += 1
        return moved if len(moved) else None

    def isFinished(self):
        for x in range(self._size[1] - 1):
            for y in range(self._size[0] - 1):
                if self._field[y, x] == 0:
                    continue
                if (
                    self._field[y, x] == self._field[y, x + 1]
                    or self._field[y, x] == self._field[y + 1, x]
                ):
                    return False
        return True

    def __eq__(self, value):
        return (
            self._colors == value.colors
            and self._size == value.size
            and np.all(self._field == value.field)
        )

    def __repr__(self):
        return f"DotsGame(colors={self._colors},size={self._size})"
