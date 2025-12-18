# src/render/renderer.py
import pygame
from pygame import Rect, Surface

from src.world.camera import Camera
from src.world.grid import Grid
from src.world.map import TileMap, TileKind
from src.world.player import Player
from typing import Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from src.world.mummy import Mummy




class Renderer:
    def __init__(self, screen: Surface, grid: Grid):
        self.screen = screen
        self.grid = grid
        self.font = pygame.font.Font(None, 28)

    def draw_world(self, *, tilemap: TileMap, player: Player, camera: Camera,
                   score: int, mummies: Sequence["Mummy"],exit_pos: tuple[int, int],level: int,) -> None:
        ts = self.grid.tile_size
        screen_rect = self.screen.get_rect()

        start_gx = max(0, camera.x // ts)
        start_gy = max(0, camera.y // ts)
        end_gx = min(tilemap.w, (camera.x + screen_rect.w) // ts + 2)
        end_gy = min(tilemap.h, (camera.y + screen_rect.h) // ts + 2)

        self.screen.fill((12, 12, 16))

        for gy in range(start_gy, end_gy):
            for gx in range(start_gx, end_gx):
                t = tilemap.tiles[gy][gx]
                wx, wy = gx * ts, gy * ts
                sx, sy = wx - camera.x, wy - camera.y
                r = Rect(sx, sy, ts, ts)

                if t == TileKind.WALL:
                    pygame.draw.rect(self.screen, (70, 70, 85), r)
                else:
                    pygame.draw.rect(self.screen, (25, 25, 33), r)

                # Si no está destapada, la "tapo"
                if not tilemap.revealed[gy][gx] and t == TileKind.FLOOR:
                    pygame.draw.rect(self.screen, (8, 8, 10), r)

                pygame.draw.rect(self.screen, (18, 18, 24), r, 1)

        ex, ey = exit_pos
        ewx, ewy = ex * ts, ey * ts
        esx, esy = ewx - camera.x, ewy - camera.y
        er = Rect(esx + 2, esy + 2, ts - 4, ts - 4)
        pygame.draw.rect(self.screen, (80, 170, 80), er, 2)

        # Player
        pwx, pwy = player.gx * ts, player.gy * ts
        psx, psy = pwx - camera.x, pwy - camera.y
        pr = Rect(psx + 4, psy + 4, ts - 8, ts - 8)
        pygame.draw.rect(self.screen, (220, 220, 120), pr)

        # Mummies
        for m in mummies:
            mwx, mwy = m.gx * ts, m.gy * ts
            msx, msy = mwx - camera.x, mwy - camera.y
            mr = Rect(msx + 6, msy + 6, ts - 12, ts - 12)
            pygame.draw.rect(self.screen, (170, 80, 80), mr)

        # HUD
        hud = self.font.render(f"Score: {score}", True, (240, 240, 240))
        self.screen.blit(hud, (10, 10))
        hud2 = self.font.render(f"Lives: {player.lives}", True, (240, 240, 240))
        self.screen.blit(hud2, (10, 34))
        hud_lvl = self.font.render(f"Level: {level}", True, (240, 240, 240))
        self.screen.blit(hud_lvl, (10, 58))





