# src/world/player.py
from dataclasses import dataclass

from .map import TileMap

@dataclass
class Player:
    gx: int
    gy: int
    last_step_ms: int = 0

    def try_step(self, *, dx: int, dy: int, tilemap: TileMap) -> None:
        nx, ny = self.gx + dx, self.gy + dy
        if tilemap.is_walkable(nx, ny):
            self.gx, self.gy = nx, ny
