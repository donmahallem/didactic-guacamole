import sys
from guacamole.base_game import BaseGame
from abc import ABC
from OpenGL import GL, GLU
import glm
import glfw
from guacamole.constants import (
    KEY_DELTA_T,
    SCREEN_BASE_WIDTH,
    SCREEN_BASE_HEIGHT,
    KEY_MOUSE_POS,
    KEY_CLICKED_AT,
)
from guacamole.shaders import (
    TriangulateShader,
    PixelateShader,
    RectShader,
    LightHouseShader,
)
from guacamole.fps_counter import Timer


class BaseApp(ABC):
    def __init__(
        self,
        screen_size=(600, 600 * SCREEN_BASE_HEIGHT / SCREEN_BASE_WIDTH),
        game_size=(SCREEN_BASE_WIDTH, SCREEN_BASE_HEIGHT),
    ):
        if not glfw.init():
            raise Exception("GLFW can't be initialized")
        self.game_size = (int(game_size[0]), int(game_size[1]))
        self.screen_size = (int(screen_size[0]), int(screen_size[1]))
        self.window1 = glfw.create_window(
            self.screen_size[0], self.screen_size[1], "Didactic Guacamole", None, None
        )
        if not self.window1:
            glfw.terminate()
            raise Exception("GLFW window can't be created")
        glfw.set_window_aspect_ratio(self.window1, self.game_size[0], self.game_size[1])
        glfw.make_context_current(self.window1)
        glfw.set_window_size_callback(self.window1, self.onWindowResize)
        glfw.set_key_callback(self.window1, self.onKeyboardInput)
        glfw.set_mouse_button_callback(self.window1, self.onMouseButton)
        self.basegame = self.initGame()
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GLU.gluOrtho2D(0, SCREEN_BASE_WIDTH, 0, SCREEN_BASE_HEIGHT)
        self.pixel_shader = LightHouseShader(self.screen_size)
        self.fpsCounter = Timer()
        self._messagQueue = list()

    def initGame(self) -> BaseGame:
        return BaseGame(self.game_size[0], self.game_size[0])

    def draw(self) -> None:
        # GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.pixel_shader.frameBuffer)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        # GL.glTranslatef(0.0, 0.0, -5)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glViewport(0, 0, self.screen_size[0], self.screen_size[1])
        # GL.glLoadIdentity()
        GLU.gluOrtho2D(0, SCREEN_BASE_WIDTH, 0, SCREEN_BASE_HEIGHT)
        # GL.glLoadIdentity()
        GL.glMatrixMode(GL.GL_MODELVIEW)
        self.basegame.draw()
        # GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        # self.pixel_shader.draw()
        glfw.swap_buffers(self.window1)

    def run(self) -> None:
        while not glfw.window_should_close(self.window1):
            deltaT = self.fpsCounter.tick()
            mouse_pos = glm.vec2(glfw.get_cursor_pos(self.window1))
            mouse_pos /= self.screen_size
            args = dict()
            args[KEY_DELTA_T] = deltaT
            args[KEY_MOUSE_POS] = mouse_pos
            while len(self._messagQueue) > 0:
                key, val = self._messagQueue.pop(0)
                args[key] = val

            self.basegame.update(**args)
            self.draw()
            # self.pixel_shader.draw()
            glfw.poll_events()

    def onWindowResize(self, window, width, height) -> None:
        self.screen_size = (width, height)
        GL.glViewport(0, 0, width, height)

    def onKeyboardInput(self, window, key: int, scancode: int, action: int, mods: int):
        print(key, scancode, action, mods)

    def onMouseButton(self, window, key: int, action: int, mods: int):
        if key == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            mousePos = glm.vec2(glfw.get_cursor_pos(window))
            mousePos /= self.screen_size
            # invert item
            mousePos.y = 1 - mousePos.y
            self._messagQueue.append((KEY_CLICKED_AT, mousePos))

    def close(self) -> None:
        sys.exit()
