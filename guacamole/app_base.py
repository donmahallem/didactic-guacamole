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
    KEY_MOVE_BOTTOM,
    KEY_MOVE_TOP,
    KEY_MOVE_LEFT,
    KEY_MOVE_RIGHT,
    KEY_SELECT,
    KEY_RESET_GAME,
)
from guacamole.shaders import (
    TriangulateShader,
    PixelateShader,
    RectShader,
    LightHouseShader,
)
from guacamole.fps_counter import Timer
from guacamole.shaders.util import create_shader_program

vertex_shader_identy = """
#version 330
in vec2 position;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment_shader_squares = """
#version 330
uniform sampler2D screenTexture;
uniform float pixelSize;
uniform float screenHeight;
uniform float screenWidth;
out vec4 FragColor;
void main() {
    vec2 uv = gl_FragCoord.xy / vec2(screenWidth, screenHeight);
    vec2 pixelatedUV = floor(uv / pixelSize) * pixelSize;
    FragColor = texture(screenTexture, pixelatedUV);
}
"""


class BaseApp(ABC):
    def __init__(
        self,
        screen_size=(600, 600 * SCREEN_BASE_HEIGHT / SCREEN_BASE_WIDTH),
        game_size=(SCREEN_BASE_WIDTH, SCREEN_BASE_HEIGHT),
        colors=4,
        seed=None,
    ):
        print(f"Game started with {colors} and seed {seed}")
        self._colors = colors
        self._seed = seed
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
        glfw.make_context_current(self.window1)
        glfw.set_window_aspect_ratio(self.window1, self.game_size[0], self.game_size[1])
        glfw.set_window_size_callback(self.window1, self.onWindowResize)
        glfw.set_key_callback(self.window1, self.onKeyboardInput)
        glfw.set_mouse_button_callback(self.window1, self.onMouseButton)
        self.basegame = self.initGame()
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GLU.gluOrtho2D(0, SCREEN_BASE_WIDTH, 0, SCREEN_BASE_HEIGHT)
        self._pixelShader = create_shader_program(
            vertex_shader_identy, fragment_shader_squares
        )
        self._fpsCounter = Timer()
        self._messagQueue = list()

    def initGame(self) -> BaseGame:
        return BaseGame(
            self.game_size[0], self.game_size[0], colors=self._colors, seed=self._seed
        )

    def draw(self) -> None:
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LEQUAL)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glViewport(0, 0, self.screen_size[0], self.screen_size[1])
        GLU.gluOrtho2D(0, SCREEN_BASE_WIDTH, 0, SCREEN_BASE_HEIGHT)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glUseProgram(self._pixelShader)
        self.basegame.draw()
        GL.glUseProgram(0)
        glfw.swap_buffers(self.window1)

    def run(self) -> None:
        while not glfw.window_should_close(self.window1):
            deltaT = self._fpsCounter.tick()
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
        if key == glfw.KEY_A and action == glfw.PRESS:
            self._messagQueue.append((KEY_MOVE_LEFT, True))
        elif key == glfw.KEY_S and action == glfw.PRESS:
            self._messagQueue.append((KEY_MOVE_BOTTOM, True))
        elif key == glfw.KEY_D and action == glfw.PRESS:
            self._messagQueue.append((KEY_MOVE_RIGHT, True))
        elif key == glfw.KEY_W and action == glfw.PRESS:
            self._messagQueue.append((KEY_MOVE_TOP, True))
        elif key == glfw.KEY_SPACE and action == glfw.PRESS:
            self._messagQueue.append((KEY_SELECT, True))
        elif key == glfw.KEY_R and action == glfw.PRESS:
            self._messagQueue.append((KEY_RESET_GAME, True))

    def onMouseButton(self, window, key: int, action: int, mods: int):
        if key == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            mousePos = glm.vec2(glfw.get_cursor_pos(window))
            mousePos /= self.screen_size
            # invert item
            mousePos.y = 1 - mousePos.y
            self._messagQueue.append((KEY_CLICKED_AT, mousePos))

    def close(self) -> None:
        sys.exit()
