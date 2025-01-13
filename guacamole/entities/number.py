from OpenGL import GL
from guacamole.constants import (
    KEY_MOUSE_POS,
    KEY_DELTA_T,
)
from .sprite import Sprite
from guacamole.shaders.util import create_shader_program, loadTextureGrey
import glm
import math
import json
import codecs

with codecs.open("./guacamole/entities/texture_num.json", mode="r") as f:
    LETTER_COORDS = json.load(f)


class Number(Sprite):
    def __init__(self, size=(1, 1)):
        super().__init__()
        self.scale.xy = size
        self._letterCoordStart = glm.vec2(0)
        self._letterCoordEnd = glm.vec2(1)
        self._displaySize = glm.vec2(1)
        self.displayNumber = 0

        self._texture = loadTextureGrey("./guacamole/entities/texture_num.png")
        self._animTime = 0

    @property
    def displaySize(self) -> glm.vec2:
        return self._displaySize

    @property
    def displayNumber(self):
        return self._displayNumber

    @displayNumber.setter
    def displayNumber(self, val):
        self._displayNumber = val
        WIDTH = 5 * 128
        HEIGHT = 2 * 128
        keyVal = str(val)
        self._letterCoordStart.xy = (
            LETTER_COORDS[keyVal][0] / WIDTH,
            1 - (LETTER_COORDS[keyVal][1] / HEIGHT),
        )
        self._letterCoordEnd.xy = (
            LETTER_COORDS[keyVal][2] / WIDTH,
            1 - (LETTER_COORDS[keyVal][3] / HEIGHT),
        )
        self._displaySize.x = (LETTER_COORDS[keyVal][2] - LETTER_COORDS[keyVal][0]) / (
            LETTER_COORDS[keyVal][3] - LETTER_COORDS[keyVal][1]
        )

    def __repr__(self):
        return f"NumberSprite({self.displayNumber})"

    def draw(self):
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)
        GL.glPushMatrix()
        GL.glTranslatef(self.position.x, self.position.y, self.position.z)
        GL.glScalef(self.scale.x, self.scale.y, self.scale.z)
        # GL.glUseProgram(self._shader)
        GL.glColor3f(1, 0, 0)
        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord2f(self._letterCoordStart.x, self._letterCoordEnd.y)
        GL.glVertex2f(0, 0)
        GL.glColor3f(1, 0, 1)
        GL.glTexCoord2f(self._letterCoordEnd.x, self._letterCoordEnd.y)
        GL.glVertex2f(1, 0)
        GL.glColor3f(1, 1, 1)
        GL.glTexCoord2f(self._letterCoordEnd.x, self._letterCoordStart.y)
        GL.glVertex2f(1, 1)
        GL.glColor3f(0, 0, 1)
        GL.glTexCoord2f(self._letterCoordStart.x, self._letterCoordStart.y)
        GL.glVertex2f(0, 1)
        GL.glEnd()
        # GL.glUseProgram(0)
        GL.glPopMatrix()
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glDisable(GL.GL_TEXTURE_2D)

        GL.glDisable(GL.GL_BLEND)
