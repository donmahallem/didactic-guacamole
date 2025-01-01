import pygame
import sys
from base_game import BaseGame
from abc import ABC
from OpenGL.GL import *
from OpenGL.GLU import *
from constants import KEY_DELTA_T

PIXEL_NUM_HORIZONTAL = 28
PIXEL_NUM_VERTICAL = 14
PIXEL_SIZE_HORIZONTAL = 97.6
PIXEL_SPACING_HORIZONTAL = 42.9
PIXEL_SIZE_VERTICAL = 161
PIXEL_SPACING_VERTICAL = 162.8

SCREEN_BASE_WIDTH = (
    PIXEL_NUM_HORIZONTAL * PIXEL_SIZE_HORIZONTAL
    + (PIXEL_NUM_HORIZONTAL - 1) * PIXEL_SPACING_HORIZONTAL
)
SCREEN_BASE_HEIGHT = (
    PIXEL_NUM_VERTICAL * PIXEL_SIZE_VERTICAL
    + (PIXEL_NUM_VERTICAL - 1) * PIXEL_SPACING_VERTICAL
)


class BaseApp(ABC):
    def __init__(self, GAME_WIDTH=SCREEN_BASE_WIDTH, GAME_HEIGHT=SCREEN_BASE_HEIGHT):
        pygame.init()
        self.game_width = GAME_WIDTH
        self.game_height = GAME_HEIGHT
        self.clock = pygame.time.Clock()
        self.screen = self.initScreen()
        self.basegame = self.initGame()
        pygame.display.set_caption("Didactic Guacamole")
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        gluOrtho2D(0, GAME_WIDTH, 0, GAME_HEIGHT)

    def initScreen(self) -> pygame.surface.Surface:
        return pygame.display.set_mode(
            (self.game_width, self.game_height), flags=pygame.DOUBLEBUF | pygame.OPENGL
        )

    def initGame(self) -> BaseGame:
        return BaseGame(self.game_width, self.game_height)

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            deltaT = self.clock.tick()
            # Clear the screen
            self.basegame.update(**{KEY_DELTA_T: deltaT})
            self.basegame.draw()
            pygame.display.flip()
            # Update the display

    def close(self) -> None:
        pygame.quit()
        sys.exit()
