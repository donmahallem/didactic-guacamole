from guacamole.entities import Player, GradientBackground
from guacamole.constants import PIXEL_SIZE_HORIZONTAL, PIXEL_SIZE_VERTICAL
from guacamole.util import Rect
from guacamole.entities.group import Group
from guacamole.entities.box import Box, Entity
from guacamole.entities.water import Water
from guacamole.entities.dots import DotsGameEntity
import glfw


class BaseGame(Group):
    def __init__(self, width, height, *sprites):
        super().__init__(*sprites)
        self.background = GradientBackground()
        self.background.position.z = 1
        self.add(self.background)
        self.item = DotsGameEntity()
        self.item.position = (0, 0, 0)
        self.add(self.item)

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
