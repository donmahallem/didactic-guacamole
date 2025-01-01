import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import numpy as np


class CircleSprite:
    def __init__(self, x, y, width, height):
        self.center = pygame.math.Vector2(x, y)
        self.radius = pygame.math.Vector2(width, height)
        self.color = (1, 0, 0, 1)
        self._vertexBuffer = glGenBuffers(1)
        self.splits = 100
        if width == height:
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

        glColor4f(w, x, y, z)
        glPushMatrix()
        glTranslatef(self.center.x, self.center.y, 0)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertexBuffer)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, None)
        glDrawArrays(GL_POLYGON, 0, 360)
        glDisableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glPopMatrix()

    def __generateElipse(self):
        vertices = []
        for i in range(self.splits):
            theta = i * 3.14159 / (self.splits / 2)
            vertices.append(self.radius.x * math.cos(theta))
            vertices.append(self.radius.y * math.sin(theta))
        vertices = np.array(vertices, dtype=np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertexBuffer)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def __generateCircle(self):
        vertices = []
        for i in range(self.splits):
            theta = i * 3.14159 / (self.splits / 2)
            vertices.append(self.radius.x * math.cos(theta))
            vertices.append(self.radius.x * math.sin(theta))
        vertices = np.array(vertices, dtype=np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertexBuffer)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
