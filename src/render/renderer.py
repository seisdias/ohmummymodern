# src/render/renderer.py
import pygame
from pygame import Rect, Surface

from src.world.camera import Camera
from src.world.grid import Grid
from src.world.map import TileMap
from src.world.player import Player

class Renderer:
    def __init__(self, screen: Surface, grid: Grid):
        self.screen = screen
        self.grid = grid

    def draw_world(self, *, tilemap: TileMap, player: Player, camera: Camera) -> None:
        ts = self.grid.tile_size
        screen_rect = self.screen.get_rect()

        # Visible tiles range (culling)
        start_gx = max(0, camera.x // ts)
        start_gy = max(0, camera.y // ts)
        end_gx = min(tilemap.w, (camera.x + screen_rect.w) // ts + 2)
        end_gy = min(tilemap.h, (camera.y + screen_rect.h) // ts + 2)

        # Fondo
        self.screen.fill((12, 12, 16))

        # Tiles
        for gy in range(start_gy, end_gy):
            for gx in range(start_gx, end_gx):
                t = tilemap.tiles[gy][gx]
                wx, wy = gx * ts, gy * ts
                sx, sy = wx - camera.x, wy - camera.y
                r = Rect(sx, sy, ts, ts)

                if t == 1:  # pared
                    pygame.draw.rect(self.screen, (70, 70, 85), r)
                else:       # suelo
                    pygame.draw.rect(self.screen, (25, 25, 33), r)

                # rejilla suave (debug visual)
                pygame.draw.rect(self.screen, (18, 18, 24), r, 1)

        # Player
        pwx, pwy = player.gx * ts, player.gy * ts
        psx, psy = pwx - camera.x, pwy - camera.y
        pr = Rect(psx + 4, psy + 4, ts - 8, ts - 8)
        pygame.draw.rect(self.screen, (220, 220, 120), pr)
