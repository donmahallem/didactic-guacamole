import pygame
import sys
from base_game import BaseGame
from abc import ABC
from OpenGL.GL import *
from OpenGL.GLU import *
from constants import KEY_DELTA_T, SCREEN_BASE_WIDTH, SCREEN_BASE_HEIGHT


class BaseApp(ABC):
    def __init__(
        self,
        screen_size=(600, int(600 / SCREEN_BASE_WIDTH * SCREEN_BASE_HEIGHT)),
        game_size=(SCREEN_BASE_WIDTH, SCREEN_BASE_HEIGHT),
    ):
        pygame.init()
        self.game_size = game_size
        self.screen_size = screen_size
        self.clock = pygame.time.Clock()
        self.screen = self.initScreen()
        self.basegame = self.initGame()
        pygame.display.set_caption("Didactic Guacamole")
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        gluOrtho2D(0, SCREEN_BASE_WIDTH, 0, SCREEN_BASE_HEIGHT)

    def initScreen(self) -> pygame.surface.Surface:
        return pygame.display.set_mode(
            self.screen_size, flags=pygame.DOUBLEBUF | pygame.OPENGL
        )

    def initGame(self) -> BaseGame:
        return BaseGame(self.game_size[0], self.game_size[0])

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
