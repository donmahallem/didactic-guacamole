import pygame
from player import Player
from background import GradientBackground
from constants import PIXEL_SIZE_HORIZONTAL, PIXEL_SIZE_VERTICAL


class BaseGame(pygame.sprite.Group):
    def __init__(self, width, height, *sprites):
        super().__init__(*sprites)
        self.rect = pygame.rect.Rect(0, 0, width, height)
        player_size = min(PIXEL_SIZE_HORIZONTAL * 2, PIXEL_SIZE_VERTICAL * 2)
        self.player = Player(
            50, 75, player_size, player_size, pygame.rect.Rect(0, 0, width, height)
        )
        self.background = GradientBackground()
        self.add_internal(self.player)
        self.player.velocity.update(800, 450)

    def draw(self):
        self.background.draw()
        self.player.draw()
