from guacamole.entities import Player, GradientBackground
from guacamole.constants import PIXEL_SIZE_HORIZONTAL, PIXEL_SIZE_VERTICAL
from guacamole.util import Rect


class BaseGame:
    def __init__(self, width, height, *sprites):
        super().__init__(*sprites)
        self.rect = Rect(0, 0, width, height)
        player_size = min(PIXEL_SIZE_HORIZONTAL * 2, PIXEL_SIZE_VERTICAL * 2)
        self.player = Player(
            (50, 75), (player_size, player_size), Rect(0, 0, width, height)
        )
        self.background = GradientBackground()
        self.add_internal(self.player)
        self.player.velocity.update(8000, 450)

    def draw(self):
        self.background.draw()
        self.player.draw()
