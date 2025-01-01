import pygame
from circle_sprite import CircleSprite
from constants import KEY_DELTA_T


class Player(CircleSprite):
    def __init__(self, x, y, width, height, play_area: pygame.rect.Rect):
        super().__init__(x, y, width, height)
        self.velocity = pygame.math.Vector2(10, 10)
        self.play_area = play_area

    def update(self, *args, **kwargs):
        if KEY_DELTA_T not in kwargs:
            return
        deltaT = kwargs[KEY_DELTA_T]
        self.center.x += self.velocity.x * deltaT / 1000
        self.center.y += self.velocity.y * deltaT / 1000
        moveRect = pygame.rect.Rect(
            self.play_area.topleft + self.radius,
            self.play_area.bottomright - (2 * self.radius),
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
