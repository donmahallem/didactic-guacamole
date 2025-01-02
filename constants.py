from typing import Final

KEY_DELTA_T: Final[str] = "deltaT"

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
print(
    SCREEN_BASE_WIDTH,
    SCREEN_BASE_HEIGHT,
    round(PIXEL_SPACING_HORIZONTAL / SCREEN_BASE_WIDTH, 3),
    round(PIXEL_SPACING_VERTICAL / SCREEN_BASE_HEIGHT, 3),
)
