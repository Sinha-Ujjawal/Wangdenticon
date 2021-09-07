from hashlib import md5
from typing import Tuple
import numpy as np
from PIL import Image
from PIL.Image import NEAREST

Color = Tuple[int, int, int]

WHITE = (255, 255, 255)
MIDDLE_TILES = [0, 1, 4, 5, 10, 11, 14, 15]
OPPOSITE_MAP = [0, 1, 8, 9, 4, 5, 12, 13, 2, 3, 10, 11, 6, 7, 14, 15]


def wang_tile(*, n: int, fgcolor: Color, bgcolor: Color = WHITE) -> np.array:
    n = -n if n < 0 else n

    grid = [bgcolor] * 9
    m = n % 16

    north = m & 1
    east = m & 2
    south = m & 4
    west = m & 8

    if north:
        for i in range(3):
            grid[i] = fgcolor

    if east:
        for i in range(2, 9, 3):
            grid[i] = fgcolor

    if south:
        for i in range(6, 9):
            grid[i] = fgcolor

    if west:
        for i in range(0, 7, 3):
            grid[i] = fgcolor

    return np.array(grid).reshape(3, 3, 3).astype("uint8")


def make_wangdenticon(
    *,
    name: str,
    size: int,
    gridsize: int = 5,
    bgcolor: Color = WHITE,
    invert: bool = False,
) -> Image.Image:
    hex_list = list(md5(name.encode()).digest())
    fgcolor = tuple(hex_list[:3])

    if invert:
        fgcolor, bgcolor = bgcolor, fgcolor

    middle_tile = wang_tile(
        n=MIDDLE_TILES[hex_list[-1] % len(MIDDLE_TILES)],
        fgcolor=fgcolor,
        bgcolor=bgcolor,
    )

    xub = (gridsize + 1) >> 1

    grid = [wang_tile(n=0, fgcolor=fgcolor, bgcolor=bgcolor)] * (gridsize * gridsize)

    for y in range(gridsize):
        for x in range(xub):
            left_index = y * gridsize + x
            right_index = y * gridsize + gridsize - 1 - x
            tile = hex_list[(y * xub + x) % 15]
            if left_index != right_index:
                grid[left_index] = wang_tile(
                    n=tile,
                    fgcolor=fgcolor,
                    bgcolor=bgcolor,
                )
                grid[right_index] = wang_tile(
                    n=OPPOSITE_MAP[tile % len(OPPOSITE_MAP)],
                    fgcolor=fgcolor,
                    bgcolor=bgcolor,
                )
            else:  # odd width case
                grid[left_index] = middle_tile

    grid = np.concatenate(
        [
            np.concatenate(grid[y * gridsize : y * gridsize + gridsize], axis=1)
            for y in range(gridsize)
        ],
        axis=0,
    )

    return Image.fromarray(grid).resize(size=(size, size), resample=NEAREST)
