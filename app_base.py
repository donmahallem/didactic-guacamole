import pygame
import sys
from base_game import BaseGame
from abc import ABC
from OpenGL import GL
from OpenGL.GLU import *
from constants import KEY_DELTA_T, SCREEN_BASE_WIDTH, SCREEN_BASE_HEIGHT
from pixel_shader import PixelateShader


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
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glMatrixMode(GL.GL_PROJECTION)
        gluOrtho2D(0, SCREEN_BASE_WIDTH, 0, SCREEN_BASE_HEIGHT)
        self.pixel_shader = PixelateShader(self.screen_size)

    def initScreen(self) -> pygame.surface.Surface:
        return pygame.display.set_mode(
            self.screen_size, flags=pygame.DOUBLEBUF | pygame.OPENGL
        )

    def initGame(self) -> BaseGame:
        return BaseGame(self.game_size[0], self.game_size[0])

    def draw(self) -> None:
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.pixel_shader.frameBuffer)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        self.basegame.draw()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        self.pixel_shader.draw()
        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            deltaT = self.clock.tick()
            self.basegame.update(**{KEY_DELTA_T: deltaT})
            self.draw()
            self.pixel_shader.draw()

    def close(self) -> None:
        pygame.quit()
        sys.exit()
