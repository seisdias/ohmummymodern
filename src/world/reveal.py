# src/world/reveal.py
from typing import Iterable, Tuple

from .map import TileMap, CellContent

Coord = Tuple[int, int]


def cross_coords(cx: int, cy: int) -> Iterable[Coord]:
    """Devuelve coordenadas en cruz (centro + N/S/E/O)."""
    yield cx, cy
    yield cx + 1, cy
    yield cx - 1, cy
    yield cx, cy + 1
    yield cx, cy - 1


def reveal_cross(tilemap: TileMap, cx: int, cy: int, treasure_score: int = 100) -> int:
    """
    Destapa una cruz centrada en (cx, cy).
    Devuelve los puntos obtenidos.
    """
    score = 0

    for gx, gy in cross_coords(cx, cy):
        if gx < 0 or gy < 0 or gx >= tilemap.w or gy >= tilemap.h:
            continue

        found = tilemap.reveal(gx, gy)
        if found == CellContent.TREASURE:
            score += treasure_score
            tilemap.clear_content(gx, gy)

    return score
