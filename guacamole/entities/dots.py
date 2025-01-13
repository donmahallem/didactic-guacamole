from guacamole.dots.dots_game import DotsGame
from .group import Group
from .sprite import Sprite
from .pool import Pool
from .score import ScoreDisplay
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
    KEY_MOVE_BOTTOM,
    KEY_MOVE_TOP,
    KEY_MOVE_LEFT,
    KEY_MOVE_RIGHT,
    KEY_SELECT,
)
import random
import glm
from typing import Final
from .animation import EaseInQuadAnimation, Animation
import math

SPACING_VEC: Final[glm.vec2] = glm.vec2(
    PIXEL_SPACING_HORIZONTAL, PIXEL_SPACING_VERTICAL
)
PIXEL_VEC: Final[glm.vec2] = glm.vec2(PIXEL_SIZE_HORIZONTAL, PIXEL_SIZE_VERTICAL)
SCREEN_SIZE_VEC: Final[glm.vec2] = glm.vec2(SCREEN_BASE_WIDTH, SCREEN_BASE_HEIGHT)


class CursorEntity(Sprite):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._size = glm.vec2(1)
        self._animator: Animation = EaseInQuadAnimation(0.3)
        self._animationOffset: glm.vec2 = glm.vec2(0)
        self._animationTimer = 0
        self._gamePosition = glm.vec2(0)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, s):
        self._size.xy = s

    @property
    def gamePosition(self):
        return self._gamePosition

    @gamePosition.setter
    def gamePosition(self, val):
        offset = val - self._gamePosition
        self._gamePosition.xy = val
        if self._gamePosition.x < 0:
            self._gamePosition.x = 0
        elif self._gamePosition.x >= 28:
            self._gamePosition.x = 27
        if self._gamePosition.y < 0:
            self._gamePosition.y = 0
        elif self._gamePosition.y >= 14:
            self._gamePosition.y = 13
        self.position.xy = self._gamePosition * (PIXEL_VEC + SPACING_VEC)
        self._animationOffset.xy = offset
        self._animator.reset()

    def animateFrom(self, pos: glm.vec2 | tuple[float, float]) -> None:
        self._animationOffset = pos - self.position.xy
        self._animator.reset()

    def draw(self):
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glColor4f(1.0, 1.0, 1.0, (1 + math.sin(self._animationTimer)) * 0.4 + 0.1)
        GL.glPushMatrix()
        if self._animator.done:
            GL.glTranslatef(self.position.x, self.position.y, self.position.z)
        else:
            GL.glTranslatef(
                self.position.x
                + ((1 - self._animator.progress) * self._animationOffset.x),
                self.position.y
                + ((1 - self._animator.progress) * self._animationOffset.y),
                self.position.z,
            )
        GL.glScalef(self._size.x, self._size.y, 1)
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex3f(0, 0, 0)
        GL.glVertex3f(1, 0, 0)
        GL.glVertex3f(1, 1, 0)
        GL.glVertex3f(0, 1, 0)
        GL.glEnd()
        GL.glPopMatrix()
        GL.glDisable(GL.GL_BLEND)

    def update(self, **kwargs) -> None:
        super().update(**kwargs)
        if KEY_DELTA_T in kwargs:
            if not self._animator.done:
                self._animator.update(kwargs[KEY_DELTA_T])
            self._animationTimer += kwargs[KEY_DELTA_T] * 10
        if KEY_MOVE_LEFT in kwargs:
            self.gamePosition += (-1, 0)
        if KEY_MOVE_RIGHT in kwargs:
            self.gamePosition += (1, 0)
        if KEY_MOVE_TOP in kwargs:
            self.gamePosition += (0, 1)
        if KEY_MOVE_BOTTOM in kwargs:
            self.gamePosition += (0, -1)


class DotsEntity(Sprite):
    def __init__(self, color=1, parent=None):
        super().__init__(parent)
        self._color = color
        # self._size = glm.vec2(1)
        self._animator: Animation = EaseInQuadAnimation(0.3)
        self._animationOffset: glm.vec2 = glm.vec2(0)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, c):
        self._color = c

    def animateFrom(self, pos: glm.vec2 | tuple[float, float]) -> None:
        self._animationOffset = pos - self.position.xy
        self._animator.reset()

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
        if self._animator.done:
            GL.glTranslatef(self.position.x, self.position.y, self.position.z)
        else:
            GL.glTranslatef(
                self.position.x
                + ((1 - self._animator.progress) * self._animationOffset.x),
                self.position.y
                + ((1 - self._animator.progress) * self._animationOffset.y),
                self.position.z,
            )
        GL.glScalef(self.scale.x, self.scale.y, self.scale.z)
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex3f(0, 0, 0)
        GL.glVertex3f(1, 0, 0)
        GL.glVertex3f(1, 1, 0)
        GL.glVertex3f(0, 1, 0)
        GL.glEnd()
        GL.glPopMatrix()

    def update(self, **kwargs) -> None:
        super().update(**kwargs)
        if KEY_DELTA_T in kwargs and not self._animator.done:
            self._animator.update(kwargs[KEY_DELTA_T])


class DotsPool(Pool[DotsEntity]):

    def createItem(self) -> DotsEntity:
        return DotsEntity()


class DotsGameEntity(Group):
    def __init__(self, colors=3, size=(28, 14), seed=None, parent: Group = None):
        super().__init__(parent)
        self._game: DotsGame = DotsGame(colors, size)
        self._dotsPool: DotsPool = DotsPool()
        self._map: dict[(int, int), DotsEntity] = dict()
        self._game.reset(seed)
        self.updateMatrix()
        self._cursor = CursorEntity()
        self.add(self._cursor)
        self._cursor.position.z = 0.1
        self.z = 0
        self._cursor.gamePosition = (2, 2)
        self._cursor.size = PIXEL_VEC
        self._score = ScoreDisplay()
        self._score.scale = (SCREEN_BASE_HEIGHT / 4, SCREEN_BASE_HEIGHT / 4, 1)
        self._score.position.xyz = (200, 400, 0.8)
        self.add(self._score)
        self._score.renderable = False

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
                    item.scale.xy = PIXEL_VEC
                    item.position = (SPACING_VEC + PIXEL_VEC) * (x, y)
                    self._map[pos] = item
                    self.add(item)

        print("Game contains", len(self))

    def clickedAtRelative(self, coords) -> None:
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
            self.clickedAt(translatedCoord)

    def clickedAt(self, translatedCoord) -> None:
        print(f"Clicked at cell: {translatedCoord}")
        res = self._game.dropDotsAt(translatedCoord)
        if res:
            # only update on change
            self.updateMatrix()
            for moveFrom, moveTo, _ in res[1]:
                self._map[moveTo].animateFrom(
                    (SPACING_VEC + PIXEL_VEC) * (moveFrom[1], moveFrom[0])
                )
            self._score.displayNumber = self._game.score
            if self._game.isFinished():
                print(f"Game finished with score: {self._game.score}")
                self._score.renderable = True

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if KEY_RESET_GAME in kwargs:
            self._score.renderable = False
            self._game.reset(random.random())
            self.updateMatrix()
            return
        if KEY_CLICKED_AT in kwargs:
            self.clickedAtRelative(kwargs[KEY_CLICKED_AT])
        if KEY_SELECT in kwargs:
            self.clickedAt(self._cursor.gamePosition)
