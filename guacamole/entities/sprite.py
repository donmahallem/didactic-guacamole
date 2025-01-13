"""Sample Sprite"""

import typing
import glm


class Sprite:
    """
    Simple sprite class
    """

    def __init__(self, parent: typing.Self = None, scale=(1, 1, 1)):
        self._parent = parent
        self._position = glm.vec3(0)
        self._scale = glm.vec3(scale)
        self._renderable = True

    @property
    def renderable(self) -> bool:
        return self._renderable

    @renderable.setter
    def renderable(self, state) -> None:
        self._renderable = state

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

    @x.setter
    def x(self, val):
        self._position.x = val

    @property
    def y(self):
        return self._position.y

    @y.setter
    def y(self, val):
        self._position.y = val

    @property
    def z(self):
        return self._position.z

    @z.setter
    def z(self, val):
        self._position.z = val

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, val):
        self._scale = glm.vec3(val)

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
