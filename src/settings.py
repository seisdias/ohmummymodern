# src/settings.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    screen_w: int = 960
    screen_h: int = 540
    fps: int = 60

    tile_size: int = 32
    map_w_tiles: int = 80
    map_h_tiles: int = 60

    # Movimiento por casillas: 1 tile por pulsación (step).
    player_step_cooldown_ms: int = 120  # ajustaremos luego
