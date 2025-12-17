# src/world/map.py
from dataclasses import dataclass
from typing import List

@dataclass
class TileMap:
    w: int
    h: int
    tiles: List[List[int]]  # 0 suelo, 1 pared (por ahora)

    @classmethod
    def demo(cls, w: int, h: int) -> "TileMap":
        # Mapa simple: borde de paredes + algunas paredes internas
        tiles = [[0 for _ in range(w)] for _ in range(h)]
        for y in range(h):
            for x in range(w):
                if x == 0 or y == 0 or x == w - 1 or y == h - 1:
                    tiles[y][x] = 1

        # “bultos” internos para probar colisión/cámara
        for x in range(10, 30):
            tiles[12][x] = 1
        for y in range(20, 40):
            tiles[y][25] = 1

        return cls(w=w, h=h, tiles=tiles)

    def is_walkable(self, gx: int, gy: int) -> bool:
        if gx < 0 or gy < 0 or gx >= self.w or gy >= self.h:
            return False
        return self.tiles[gy][gx] == 0
