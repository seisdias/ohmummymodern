from dataclasses import dataclass

from .map import TileMap

@dataclass
class Player:
    gx: int
    gy: int
    last_step_ms: int = 0

    lives: int = 3
    last_hit_ms: int = -10_000  # para que al inicio no esté “recién golpeado”
    hit_cooldown_ms: int = 900  # ajustable

    spawn_gx: int = 3
    spawn_gy: int = 3

    def try_step(self, *, dx: int, dy: int, tilemap: TileMap) -> None:
        nx, ny = self.gx + dx, self.gy + dy
        if tilemap.is_walkable(nx, ny):
            self.gx, self.gy = nx, ny

    def can_be_hit(self, now_ms: int) -> bool:
        return (now_ms - self.last_hit_ms) >= self.hit_cooldown_ms

    def take_hit(self, now_ms: int) -> None:
        if not self.can_be_hit(now_ms):
            return
        self.lives = max(0, self.lives - 1)
        self.last_hit_ms = now_ms
        # respawn simple
        self.gx, self.gy = self.spawn_gx, self.spawn_gy
