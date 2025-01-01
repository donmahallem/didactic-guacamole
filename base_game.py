import pygame
from player import Player
from OpenGL import GL
from constants import PIXEL_SIZE_HORIZONTAL, PIXEL_SIZE_VERTICAL


class BaseGame(pygame.sprite.Group):
    def __init__(self, width, height, *sprites):
        super().__init__(*sprites)
        self.rect = pygame.rect.Rect(0, 0, width, height)
        player_size = min(PIXEL_SIZE_HORIZONTAL, PIXEL_SIZE_VERTICAL)
        self.player = Player(
            50, 75, player_size, player_size, pygame.rect.Rect(0, 0, width, height)
        )
        self.add_internal(self.player)
        self.player.velocity.update(300, 30)

    def draw(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        self.player.draw()
