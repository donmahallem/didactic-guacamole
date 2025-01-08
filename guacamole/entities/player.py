import glm
from guacamole.constants import KEY_DELTA_T
from guacamole.util import Rect
from guacamole.entities.circle_sprite import CircleSprite


class Player(CircleSprite):
    def __init__(self, pos: tuple[float], size: tuple[float], play_area: tuple[float]):
        super().__init__(pos, size)
        self._velocity: glm.vec2 = glm.vec2(10, 10)
        if isinstance(play_area, Rect):
            self.playArea = Rect(play_area)
        else:
            self.playArea = Rect(play_area[0], play_area[1], play_area[2], play_area[3])

    @property
    def velocity(self) -> glm.vec2:
        return self._velocity

    @velocity.setter
    def velocity(self, value: glm.vec2 | tuple[float, float]):
        if isinstance(value, glm.vec2):
            self._velocity = glm.vec2(value)
        elif isinstance(value, tuple):
            self._velocity = glm.vec2(value[0], value[1])
        else:
            raise ValueError("2D Vector required")

    def update(self, *args, **kwargs):
        if KEY_DELTA_T not in kwargs:
            return
        deltaT = kwargs[KEY_DELTA_T]
        self.center += self._velocity * deltaT
        moveRect = Rect(
            self.playArea.topLeft + self.radius,
            self.playArea.bottomRight - self.radius,
        )
        while not moveRect.pointInside(self.center):
            if self.center.x < moveRect.left:
                self.center.x = moveRect.left + (moveRect.left - self.center.x)
                self._velocity.x = abs(self._velocity.x)
            if self.center.y < moveRect.top:
                self.center.y = moveRect.top + (moveRect.top - self.center.y)
                self._velocity.y = abs(self._velocity.y)
            if self.center.y > moveRect.bottom:
                self.center.y = moveRect.bottom - (self.center.y - moveRect.bottom)
                self._velocity.y = -abs(self._velocity.y)
            if self.center.x > moveRect.right:
                self.center.x = moveRect.right - (self.center.x - moveRect.right)
                self._velocity.x = -abs(self._velocity.x)
