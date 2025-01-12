import random
import numpy as np


class Maze:
    def __init__(self, size: tuple[int, int]) -> None:
        self._size = size
        self._maze = np.zeroes(self._size, dtype=np.uint8)

    def manhattenDistance(self, a, b) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def initWilson(self, seed: str | int = random.random()) -> None:
        self._maze *= 0
        rnd = np.random.default_rng(seed)
        # run until reasonable start and end points found
        while True:
            start = (rnd.integers(0, self._size[0]), rnd.integers(0, self._size[1]))
            end = (rnd.integers(0, self._size[0]), rnd.integers(0, self._size[1]))
            if start != end and self.manhattenDistance(start, end) > 1:
                break

        def randWalkInitial(start, end):
            currentPath = [start]
            dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            while True:
                currentPosition = currentPath[-1]
                rnd.shuffle(dirs)
                for dir in dirs:
                    nextY, nextX = (
                        currentPosition[0] + dir[0],
                        currentPosition[1] + dir[1],
                    )
                    if (nextY, nextX) in currentPath:
                        continue
