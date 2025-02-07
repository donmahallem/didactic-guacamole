from typing import Final

KEY_DELTA_T: Final[str] = "deltaT"
KEY_MOUSE_POS: Final[str] = "mousePos"
KEY_RESET_GAME: Final[str] = "resetGame"
KEY_CLICKED_AT: Final[str] = "clickedAt"
KEY_MOVE_LEFT: Final[str] = "moveLeft"
KEY_MOVE_RIGHT: Final[str] = "moveRight"
KEY_MOVE_TOP: Final[str] = "moveTop"
KEY_MOVE_BOTTOM: Final[str] = "moveBottom"
KEY_SELECT: Final[str] = "select"


PIXEL_NUM_HORIZONTAL: Final[int] = 28
PIXEL_NUM_VERTICAL: Final[int] = 14
PIXEL_SIZE_HORIZONTAL: Final[float] = 97.6
PIXEL_SPACING_HORIZONTAL: Final[float] = 42.9
PIXEL_SIZE_VERTICAL: Final[float] = 161
PIXEL_SPACING_VERTICAL: Final[float] = 162.8

SCREEN_BASE_WIDTH: Final[float] = (
    PIXEL_NUM_HORIZONTAL * PIXEL_SIZE_HORIZONTAL
    + (PIXEL_NUM_HORIZONTAL - 1) * PIXEL_SPACING_HORIZONTAL
)
SCREEN_BASE_HEIGHT: Final[float] = (
    PIXEL_NUM_VERTICAL * PIXEL_SIZE_VERTICAL
    + (PIXEL_NUM_VERTICAL - 1) * PIXEL_SPACING_VERTICAL
)
