class Animation:
    def __init__(self, time):
        self._runTime = time
        self.reset()

    def reset(self) -> None:
        self._progress = 0
        self._elapsedTime = 0
        self._done = False

    @property
    def done(self) -> bool:
        return self._done

    @property
    def progress(self) -> float:
        return self._progress

    def calculateProgress(self) -> float:
        return self._elapsedTime / self._runTime

    def update(self, deltaT) -> None:
        self._elapsedTime += deltaT
        if self._elapsedTime >= self._runTime:
            self._done = True
            self._progress = 1
        else:
            self._progress = self.calculateProgress()


class EaseInQuadAnimation(Animation):

    def calculateProgress(self):
        return (self._elapsedTime / self._runTime) ** 2
