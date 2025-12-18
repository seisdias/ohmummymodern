# src/game.py
import pygame

from src.settings import Settings
from src.world.grid import Grid
from src.world.camera import Camera
from src.world.map import TileMap, CellContent
from src.world.player import Player
from src.render.renderer import Renderer


class Game:
    def __init__(self, screen: pygame.Surface, settings: Settings):
        self.screen = screen
        self.s = settings

        self.grid = Grid(tile_size=self.s.tile_size)
        self.tilemap = TileMap.demo(self.s.map_w_tiles, self.s.map_h_tiles)

        self.player = Player(gx=3, gy=3)
        self.camera = Camera()

        self.renderer = Renderer(screen, self.grid)

        self.world_w_px = self.tilemap.w * self.s.tile_size
        self.world_h_px = self.tilemap.h * self.s.tile_size

        self.score = 0

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            found = self.tilemap.reveal(self.player.gx, self.player.gy)
            if found == CellContent.TREASURE:
                self.score += 100
                self.tilemap.clear_content(self.player.gx, self.player.gy)

    def handle_input(self, now_ms: int) -> None:
        keys = pygame.key.get_pressed()
        if now_ms - self.player.last_step_ms < self.s.player_step_cooldown_ms:
            return

        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1

        if dx != 0 or dy != 0:
            self.player.try_step(dx=dx, dy=dy, tilemap=self.tilemap)
            self.player.last_step_ms = now_ms

    def update(self) -> None:
        ts = self.s.tile_size
        target_x = self.player.gx * ts + ts // 2
        target_y = self.player.gy * ts + ts // 2

        self.camera.follow_and_clamp(
            target_x=target_x,
            target_y=target_y,
            screen_w=self.s.screen_w,
            screen_h=self.s.screen_h,
            world_w=self.world_w_px,
            world_h=self.world_h_px,
        )

    def draw(self) -> None:
        self.renderer.draw_world(
            tilemap=self.tilemap,
            player=self.player,
            camera=self.camera,
            score=self.score,
        )
        pygame.display.flip()
