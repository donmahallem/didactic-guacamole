import os
import OpenGL

if os.environ.get("TEST_NO_ACCELERATE"):
    OpenGL.USE_ACCELERATE = False
from OpenGL import GL
from guacamole.constants import SCREEN_BASE_HEIGHT, SCREEN_BASE_WIDTH


VERTEX_BUFFER = 0
COLOR_BUFFER = 1


class GradientBackground:
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
