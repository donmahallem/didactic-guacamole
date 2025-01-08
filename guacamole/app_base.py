import sys
from guacamole.base_game import BaseGame
from abc import ABC
from OpenGL import GL, GLU
import glfw
from guacamole.constants import KEY_DELTA_T, SCREEN_BASE_WIDTH, SCREEN_BASE_HEIGHT
from guacamole.shaders import (
    TriangulateShader,
    PixelateShader,
    RectShader,
    LightHouseShader,
)


class BaseApp(ABC):
    def __init__(
        self,
        screen_size=(600, 600 * SCREEN_BASE_HEIGHT / SCREEN_BASE_WIDTH),
        game_size=(SCREEN_BASE_WIDTH, SCREEN_BASE_HEIGHT),
    ):
        if not glfw.init():
            raise Exception("GLFW can't be initialized")
        self.fpsDisplayInterval = 2
        self.game_size = (int(game_size[0]), int(game_size[1]))
        self.screen_size = (int(screen_size[0]), int(screen_size[1]))
        self.window1 = glfw.create_window(
            self.screen_size[0], self.screen_size[1], "Didactic Guacamole", None, None
        )
        if not self.window1:
            glfw.terminate()
            raise Exception("GLFW window can't be created")
        glfw.make_context_current(self.window1)
        self.basegame = self.initGame()
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GLU.gluOrtho2D(0, SCREEN_BASE_WIDTH, 0, SCREEN_BASE_HEIGHT)
        self.pixel_shader = LightHouseShader(self.screen_size)

    def initGame(self) -> BaseGame:
        return BaseGame(self.game_size[0], self.game_size[0])

    def draw(self) -> None:
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.pixel_shader.frameBuffer)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        self.basegame.draw()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        self.pixel_shader.draw()
        glfw.swap_buffers(self.window1)

    def run(self) -> None:
        running = True
        lastTime = glfw.get_time()
        fpsTimer = 0
        while not glfw.window_should_close(self.window1):
            timeNow = glfw.get_time()
            deltaT = timeNow - lastTime
            # print(glfw.get_time(),fpsTimer)
            self.basegame.update(**{KEY_DELTA_T: deltaT})
            self.draw()
            # self.pixel_shader.draw()
            fpsTimer += deltaT
            if fpsTimer >= self.fpsDisplayInterval:
                print(f"FPS: {1/deltaT:.2f}")
                fpsTimer = 0
            lastTime = timeNow
            glfw.poll_events()

    def close(self) -> None:
        sys.exit()
