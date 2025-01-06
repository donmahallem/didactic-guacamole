import glm
from guacamole.constants import KEY_DELTA_T
from guacamole.util import Rect
from .circle_sprite import CircleSprite


class Player(CircleSprite):
    def __init__(self, pos: tuple[float], size: tuple[float], play_area: tuple[float]):
        super().__init__(pos, size)
        self.velocity = glm.vec2(10, 10)
        if isinstance(play_area) == Rect:
            self.playArea = Rect(play_area)
        else:
            self.playArea = Rect(play_area[0], play_area[1], play_area[2], play_area[3])

    def update(self, *args, **kwargs):
        if KEY_DELTA_T not in kwargs:
            return
        deltaT = kwargs[KEY_DELTA_T]
        self.center.x += self.velocity.x * deltaT / 1000
        self.center.y += self.velocity.y * deltaT / 1000
        moveRect = Rect(
            self.playArea.topLeft + self.radius,
            self.playArea.bottomRight - (2 * self.radius),
        )
        while not moveRect.collidepoint(self.center):
            if self.center.x < moveRect.left:
                self.center.x = moveRect.left + (moveRect.left - self.center.x)
                self.velocity.x = abs(self.velocity.x)
            if self.center.y < moveRect.top:
                self.center.y = moveRect.top + (moveRect.top - self.center.y)
                self.velocity.y = abs(self.velocity.y)
            if self.center.y > moveRect.bottom:
                self.center.y = moveRect.bottom - (self.center.y - moveRect.bottom)
                self.velocity.y = -abs(self.velocity.y)
            if self.center.x > moveRect.right:
                self.center.x = moveRect.right - (self.center.x - moveRect.right)
                self.velocity.x = -abs(self.velocity.x)
