from guacamole.dots.dots_game import DotsGame
from .group import Group
from .sprite import Sprite
from .pool import Pool
from OpenGL import GL
from guacamole.constants import (
    KEY_RESET_GAME,
    KEY_DELTA_T,
    KEY_CLICKED_AT,
    PIXEL_SIZE_HORIZONTAL,
    PIXEL_SIZE_VERTICAL,
    PIXEL_SPACING_HORIZONTAL,
    PIXEL_SPACING_VERTICAL,
    SCREEN_BASE_HEIGHT,
    SCREEN_BASE_WIDTH,
)
import random
import glm
from typing import Final

SPACING_VEC: Final[glm.vec2] = glm.vec2(
    PIXEL_SPACING_HORIZONTAL, PIXEL_SPACING_VERTICAL
)
PIXEL_VEC: Final[glm.vec2] = glm.vec2(PIXEL_SIZE_HORIZONTAL, PIXEL_SIZE_VERTICAL)
SCREEN_SIZE_VEC: Final[glm.vec2] = glm.vec2(SCREEN_BASE_WIDTH, SCREEN_BASE_HEIGHT)


class DotsEntity(Sprite):
    def __init__(self, color=1, parent=None):
        super().__init__(parent)
        self._color = color
        self._size = glm.vec2(1)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, s):
        self._size.xy = s

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, c):
        self._color = c

    def draw(self):
        if self._color == 1:
            GL.glColor3f(1.0, 0.0, 0.0)
        elif self._color == 2:
            GL.glColor3f(0.0, 1.0, 0.0)
        elif self._color == 3:
            GL.glColor3f(0.0, 0.0, 1.0)
        elif self._color == 4:
            GL.glColor3f(1.0, 1.0, 0.0)
        elif self._color == 5:
            GL.glColor3f(0.0, 1.0, 1.0)
        elif self._color == 6:
            GL.glColor3f(1.0, 0.0, 1.0)
        GL.glPushMatrix()
        GL.glTranslatef(self.position.x, self.position.y, self.position.z)
        GL.glScalef(self._size.x,self._size.y,0)
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex2f(0, 0)
        GL.glVertex2f(1, 0)
        GL.glVertex2f(1, 1)
        GL.glVertex2f(0, 1)
        GL.glEnd()
        GL.glPopMatrix()


class DotsPool(Pool[DotsEntity]):

    def createItem(self) -> DotsEntity:
        return DotsEntity()


class DotsGameEntity(Group):
    def __init__(self, colors=3, size=(28, 14), parent=None):
        super().__init__(parent)
        self._game = DotsGame(colors, size)
        self._dotsPool = DotsPool()
        self._map = dict()
        self._game.reset(292)
        self.updateMatrix()

    def updateMatrix(self):
        for y in range(self._game.size[1]):
            for x in range(self._game.size[0]):
                pos = (y, x)
                expectedColor = self._game[pos]
                if pos in self._map:
                    actual = self._map[pos]
                    if expectedColor > 0:
                        actual.color = expectedColor
                    else:
                        self.remove(actual)
                        self._dotsPool.returnItem(actual)
                        del self._map[pos]
                elif expectedColor > 0:
                    item = self._dotsPool.getItem()
                    item.color = expectedColor
                    item.size = PIXEL_VEC
                    item.position = (SPACING_VEC + PIXEL_VEC) * (x, y)
                    self._map[pos] = item
                    self.add(item)

        print("Game contains", len(self))

    def clickedAt(self, coords) -> None:
        cellOffset = PIXEL_VEC + SPACING_VEC
        totalSize = cellOffset * self._game.size
        translatedCoord = coords * SCREEN_SIZE_VEC
        translatedCoord = translatedCoord / totalSize * self._game.size
        fractionalCoord = translatedCoord % 1
        fractSize = PIXEL_VEC / cellOffset
        if sum(fractionalCoord > fractSize) > 0:
            return
        else:
            translatedCoord = translatedCoord // 1
            print(f"Clicked at cell: {translatedCoord}")
            res = self._game.dropDotsAt(translatedCoord)
            if res:
                # only update on change
                self.updateMatrix()
                print(res)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if KEY_RESET_GAME in kwargs:
            self._game.reset(random.random())
            self.updateMatrix()
            return
        if KEY_CLICKED_AT in kwargs:
            self.clickedAt(kwargs[KEY_CLICKED_AT])
