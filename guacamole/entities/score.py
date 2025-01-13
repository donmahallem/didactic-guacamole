from OpenGL import GL
from guacamole.constants import (
    KEY_MOUSE_POS,
    KEY_DELTA_T,
)
from .group import Group
from .number import Number
from .pool import Pool


class DotsPool(Pool[Number]):

    def createItem(self) -> Number:
        return Number()


class ScoreDisplay(Group):
    def __init__(self, size=(1, 1)):
        super().__init__()
        self.scale.xy = size
        self._letterPool = DotsPool()
        self.displayNumber = 1245
        self._animTime = 0

    @property
    def displayNumber(self):
        return self._displayNumber

    @displayNumber.setter
    def displayNumber(self, val):
        self._displayNumber = val
        displayString = str(val)
        currentOffset = 0
        for idx, ch in enumerate(displayString):
            if idx < len(self):
                numSprite = self.getChildAt(idx)
            else:
                numSprite = self._letterPool.getItem()
                self.add(numSprite)
            numSprite.displayNumber = int(ch)
            numSprite.position.x = currentOffset
            numSprite.scale.xy = numSprite.displaySize
            currentOffset += numSprite.displaySize.x + 0.1
        if len(self) > len(displayString):
            childsToRemove = self._items[len(displayString) :]
            for item in childsToRemove:
                self.remove(item)
                self._letterPool.returnItem(item)
