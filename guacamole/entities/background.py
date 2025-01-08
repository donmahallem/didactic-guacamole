from OpenGL import GL
from guacamole.constants import SCREEN_BASE_HEIGHT, SCREEN_BASE_WIDTH
from .sprite import Sprite

VERTEX_BUFFER = 0
COLOR_BUFFER = 1


class GradientBackground(Sprite):
    def __init__(self, size=(SCREEN_BASE_WIDTH, SCREEN_BASE_HEIGHT)):
        self._size = size

    def draw(self):
        GL.glBegin(GL.GL_QUADS)
        GL.glColor3f(1.0, 0.0, 0.0)  # Red
        GL.glVertex2f(0, 0)
        GL.glColor3f(0.0, 1.0, 0.0)  # Green
        GL.glVertex2f(self._size[0], 0)
        GL.glColor3f(0.0, 0.0, 1.0)  # Blue
        GL.glVertex2f(self._size[0], self._size[1])
        GL.glColor3f(1.0, 1.0, 0.0)  # Yellow
        GL.glVertex2f(0, self._size[1])
        GL.glEnd()
