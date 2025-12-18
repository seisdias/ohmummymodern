# src/world/map.py
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple
import random


class TileKind(int, Enum):
    FLOOR = 0
    WALL = 1


class CellContent(str, Enum):
    EMPTY = "empty"
    TREASURE = "treasure"


@dataclass
class TileMap:
    w: int
    h: int
    tiles: List[List[int]]                 # TileKind values (0/1)
    revealed: List[List[bool]]             # tapada/destapada
    contents: List[List[CellContent]]      # loot por casilla

    @classmethod
    def demo(cls, w: int, h: int, seed: int = 1234) -> "TileMap":
        rng = random.Random(seed)

        tiles = [[TileKind.FLOOR for _ in range(w)] for _ in range(h)]
        for y in range(h):
            for x in range(w):
                if x == 0 or y == 0 or x == w - 1 or y == h - 1:
                    tiles[y][x] = TileKind.WALL

        # “bultos” internos para probar colisión/cámara
        # (robusto a mapas pequeños, usado en tests)
        if h > 13 and w > 11:
            y_wall = min(12, h - 2)
            x_start = min(10, w - 2)
            x_end = min(30, w - 1)
            for x in range(x_start, x_end):
                tiles[y_wall][x] = TileKind.WALL

        if w > 26 and h > 21:
            x_wall = min(25, w - 2)
            y_start = min(20, h - 2)
            y_end = min(40, h - 1)
            for y in range(y_start, y_end):
                tiles[y][x_wall] = TileKind.WALL

        revealed = [[False for _ in range(w)] for _ in range(h)]
        contents: List[List[CellContent]] = [[CellContent.EMPTY for _ in range(w)] for _ in range(h)]

        # Poblamos tesoros de forma simple en suelos (solo para demo)
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if tiles[y][x] == TileKind.FLOOR:
                    # 8% tesoro (ajustable)
                    if rng.random() < 0.08:
                        contents[y][x] = CellContent.TREASURE

        return cls(w=w, h=h, tiles=tiles, revealed=revealed, contents=contents)

    def is_walkable(self, gx: int, gy: int) -> bool:
        if gx < 0 or gy < 0 or gx >= self.w or gy >= self.h:
            return False
        return self.tiles[gy][gx] == TileKind.FLOOR

    def is_revealed(self, gx: int, gy: int) -> bool:
        return self.revealed[gy][gx]

    def reveal(self, gx: int, gy: int) -> CellContent:
        """Destapa la casilla. Devuelve el contenido encontrado (si ya estaba destapada, devuelve EMPTY)."""
        if self.revealed[gy][gx]:
            return CellContent.EMPTY
        self.revealed[gy][gx] = True
        return self.contents[gy][gx]

    def clear_content(self, gx: int, gy: int) -> None:
        self.contents[gy][gx] = CellContent.EMPTY
