"""Sample Sprite"""

import typing

class Sprite:
    """
    Simple sprite class
    """
    def __init__(self, parent: typing.Self = None):
        self._parent = parent

    def draw(self):
        """Draw function"""
        pass

    def update(self, **kwargs):
        """Update function"""
        pass

    @property
    def parent(self) -> typing.Self:
        return self._parent

    @parent.setter
    def parent(self, p: typing.Self) -> None:
        self._parent = p

    def removeSelf(self) -> None:
        if self._parent:
            self._parent.remove(self)
