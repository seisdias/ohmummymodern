# src/world/grid.py
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Grid:
    tile_size: int

    def to_world(self, gx: int, gy: int) -> Tuple[int, int]:
        return gx * self.tile_size, gy * self.tile_size

    def to_grid(self, px: int, py: int) -> Tuple[int, int]:
        return px // self.tile_size, py // self.tile_size
