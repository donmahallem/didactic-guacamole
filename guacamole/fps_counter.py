import glfw
import collections
import statistics


class Timer:
    def __init__(self, debounceTime: float = 2, fpsBufferSize: int = 100):
        self._debounceTime = debounceTime
        self._lastTick = None
        self._fpsBuffer = collections.deque(maxlen=fpsBufferSize)
        self._lastOutput = 0

    @property
    def debounceTime(self) -> float:
        return self._debounceTime

    @debounceTime.setter
    def debounceTime(self, db: float) -> None:
        if db < 0:
            raise ValueError(f"{db} is to low. Debounce time must be atleast 0")
        self._debounceTime = db

    def tick(self) -> float:
        if self._lastTick == None:
            self._lastTick = glfw.get_time()
            return 0
        currentTime = glfw.get_time()
        deltaT = currentTime - self._lastTick
        fps = 1 / deltaT
        self._fpsBuffer.append(fps)
        self._lastTick = currentTime
        self._lastOutput += deltaT
        if self._lastOutput >= self._debounceTime:
            print(f"FPS(Cur: {1/deltaT:.2f} - 1%: {self.getPercentile(1):.2f})")
            self._lastOutput = self._lastOutput % self._debounceTime
        return deltaT

    def getFps(self) -> float:
        if len(self._fpsBuffer) > 0:
            return self._fpsBuffer[-1]
        return -1

    def getPercentile(self, percentile: int = 1) -> float:
        if not percentile.is_integer():
            raise ValueError("Percentile must be an integer")
        elif percentile < 0 or percentile > 98:
            raise ValueError("Percentile must be [0-98]")
        if len(self._fpsBuffer) == 0:
            return -1
        return statistics.quantiles(self._fpsBuffer, n=100)[percentile]
