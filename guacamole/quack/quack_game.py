import numpy as np
import random
from .quack_obstacle import QuackObstacle, QuackObstacleType
from .quack_band import QuackBand, QuackBandType
from guacamole.constants import KEY_DELTA_T, KEY_RESET_GAME


class QuackGame:
    def __init__(self):
        self._parent = None
        self._obstacleBands = dict()
        self._lastSeed = None
        self._maxPlaytime = 10
        self._playTime = 0

    def resetGame(self, seed: float | int | str = random.random()) -> None:
        self._lastSeed = hash(seed)
        self._playTime = 0
        rnd = np.random.default_rng(self._lastSeed)
        self._obstacleBands.clear()
        for bandNum in range(13):
            if bandNum % 6 != 0:
                obstacles = []
                obsType = QuackBandType.STREET if bandNum < 6 else QuackBandType.WATER
                for obstacleId in range(rnd.integers(5, 20)):
                    startPos = sum(a.size + a.position for a in obstacles) + int(
                        rnd.integers(1, 5)
                    )
                    if bandNum < 5:
                        # Its cars
                        obstacleLength = int(rnd.integers(1, 3))
                        obstacles.append(
                            QuackObstacle(
                                QuackObstacleType.CAR, startPos, obstacleLength
                            )
                        )
                    else:
                        obstacleLength = int(rnd.integers(1, 6))
                        obstacleType = rnd.choice(
                            [QuackObstacleType.TURTLE, QuackObstacleType.LOG]
                        )
                        obstacles.append(
                            QuackObstacle(obstacleType, startPos, obstacleLength)
                        )
                bandOffset = rnd.random() * 200000  # random large offset
                self._obstacleBands[bandNum] = QuackBand(
                    bandNum, obsType, bandOffset, obstacles
                )
            elif bandNum == 6:
                block = rnd.choice(14, 3)
                self._obstacleBands[bandNum] = QuackBand(bandNum, QuackBandType.SAFE, 0)
            elif bandNum == 0:
                self._obstacleBands[bandNum] = QuackBand(
                    bandNum, QuackBandType.START, 0
                )
            elif bandNum == 12:
                self._obstacleBands[bandNum] = QuackBand(bandNum, QuackBandType.END, 0)

    def getBand(self, id: int):
        return self._obstacleBands[id]

    def getBands(self) -> dict[QuackBand]:
        return self._obstacleBands

    @property
    def playTime(self) -> float:
        return self._maxPlaytime

    @playTime.setter
    def playTime(self, playtime: float) -> None:
        if playtime > 0:
            self._maxPlaytime = playtime
            return
        raise ValueError("Playtime must be greater than 0")

    def update(self, *args, **kwargs) -> None:
        if KEY_RESET_GAME in kwargs:
            self.resetGame()
            return
        if KEY_DELTA_T not in kwargs:
            return
        self._playTime += kwargs[KEY_DELTA_T]

    @property
    def lastSeed(self):
        return self._lastSeed

    @property
    def parent(self) -> None:
        return self._parent

    @parent.setter
    def parent(self, parent) -> None:
        self._parent = parent
