import glm
from OpenGL import GL
import math
import numpy as np


class CircleSprite:
    def __init__(self, pos, size):
        self.center = glm.vec2(pos[0], pos[0])
        self.radius = glm.vec2(size[0], size[1])
        self.color = (1, 0, 0, 1)
        self._vertexBuffer = GL.glGenBuffers(1)
        self.splits = 100
        if self.radius[0] == self.radius[1]:
            self.__generateCircle()
        else:
            self.__generateElipse()

    def draw(self):
        if len(self.color) == 4:
            w, x, y, z = self.color
        elif len(self.color) == 3:
            w, x, y = self.color
            z = 1
        else:
            raise ValueError(f"Invalid color: {self.color}")

        GL.glColor4f(w, x, y, z)
        GL.glPushMatrix()
        GL.glTranslatef(self.center.x, self.center.y, 0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._vertexBuffer)
        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
        GL.glVertexPointer(2, GL.GL_FLOAT, 0, None)
        GL.glDrawArrays(GL.GL_POLYGON, 0, 360)
        GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glPopMatrix()

    def __generateElipse(self):
        vertices = []
        for i in range(self.splits):
            theta = i * 3.14159 / (self.splits / 2)
            vertices.append(self.radius[0] * math.cos(theta))
            vertices.append(self.radius[1] * math.sin(theta))
        vertices = np.array(vertices, dtype=np.float32)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._vertexBuffer)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW
        )
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    def __generateCircle(self):
        vertices = []
        for i in range(self.splits):
            theta = i * 3.14159 / (self.splits / 2)
            vertices.append(self.radius[0] * math.cos(theta))
            vertices.append(self.radius[0] * math.sin(theta))
        vertices = np.array(vertices, dtype=np.float32)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._vertexBuffer)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW
        )
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
