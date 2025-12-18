# src/settings.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    screen_w: int = 960
    screen_h: int = 540
    fps: int = 60

    tile_size: int = 32


