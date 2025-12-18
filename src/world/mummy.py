# src/world/mummy.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, List

from .map import TileMap

Dir = Tuple[int, int]

DIRS_4: List[Dir] = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def manhattan(ax: int, ay: int, bx: int, by: int) -> int:
    return abs(ax - bx) + abs(ay - by)


def choose_step_towards(
    tilemap: TileMap,
    mx: int,
    my: int,
    px: int,
    py: int,
) -> Dir:
    """
    IA simple:
    - mira los 4 vecinos caminables
    - elige el que minimiza distancia Manhattan al jugador
    - en empate, mantiene orden estable (derecha, izquierda, abajo, arriba por DIRS_4)
    - si no hay movimiento posible, (0,0)
    """
    best: Dir = (0, 0)
    best_dist = manhattan(mx, my, px, py)

    for dx, dy in DIRS_4:
        nx, ny = mx + dx, my + dy
        if not tilemap.is_walkable(nx, ny):
            continue
        d = manhattan(nx, ny, px, py)
        if d < best_dist:
            best_dist = d
            best = (dx, dy)

    return best


@dataclass
class Mummy:
    gx: int
    gy: int
    move_cooldown_ms: int = 220
    last_move_ms: int = 0

    def update(self, *, tilemap: TileMap, player_gx: int, player_gy: int, now_ms: int) -> None:
        if now_ms - self.last_move_ms < self.move_cooldown_ms:
            return

        dx, dy = choose_step_towards(tilemap, self.gx, self.gy, player_gx, player_gy)
        if (dx, dy) != (0, 0):
            self.gx += dx
            self.gy += dy

        self.last_move_ms = now_ms
