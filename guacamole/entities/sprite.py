"""Sample Sprite"""

import typing
import glm


class Sprite:
    """
    Simple sprite class
    """

    def __init__(self, parent: typing.Self = None):
        self._parent = parent
        self._position = glm.vec3(0)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, v):
        if isinstance(v, glm.vec3):
            self._position = glm.vec3(v)
        elif isinstance(v, glm.vec2):
            self._position.xy = v
        elif isinstance(v, tuple) and len(v) == 2:
            self._position.xy = v
        elif isinstance(v, tuple) and len(v) == 3:
            self._position.xyz = v
        else:
            raise ValueError(f"Invalid type provided: {type(v)}")

    @property
    def x(self):
        return self._position.x

    @property
    def y(self):
        return self._position.y

    @property
    def z(self):
        return self._position.z

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
