# src/world/camera.py
from dataclasses import dataclass

@dataclass
class Camera:
    x: int = 0
    y: int = 0

    def follow_and_clamp(
        self,
        *,
        target_x: int,
        target_y: int,
        screen_w: int,
        screen_h: int,
        world_w: int,
        world_h: int,
    ) -> None:
        # Centramos en el target
        self.x = target_x - screen_w // 2
        self.y = target_y - screen_h // 2

        # Clamp a límites del mundo
        self.x = max(0, min(self.x, max(0, world_w - screen_w)))
        self.y = max(0, min(self.y, max(0, world_h - screen_h)))
