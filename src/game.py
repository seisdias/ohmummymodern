# src/game.py
import pygame

from src.settings import Settings
from src.config import GameConfig
from src.world.grid import Grid
from src.world.camera import Camera
from src.world.map import TileMap, CellContent
from src.world.player import Player
from src.render.renderer import Renderer
from src.world.reveal import reveal_cross
from src.world.mummy import Mummy
from src.world.collision import any_entity_on_player



class Game:
    def __init__(self, screen: pygame.Surface, settings: Settings, config: GameConfig):
        self.screen = screen
        self.s = settings
        self.cfg = config

        self.grid = Grid(tile_size=self.s.tile_size)
        self.tilemap = TileMap.demo(
            self.s.map_w_tiles,
            self.s.map_h_tiles,
            treasure_chance=self.cfg.treasure_chance,
        )

        self.player = Player(
            gx=3,
            gy=3,
            lives=self.cfg.player_start_lives,
            hit_cooldown_ms=self.cfg.player_hit_cooldown_ms,
            spawn_gx=3,
            spawn_gy=3,
        )
        self.mummies = [
            Mummy(gx=15, gy=15, move_cooldown_ms=self.cfg.mummy_move_cooldown_ms)
        ]
        self.camera = Camera()

        self.renderer = Renderer(screen, self.grid)

        self.world_w_px = self.tilemap.w * self.s.tile_size
        self.world_h_px = self.tilemap.h * self.s.tile_size

        self.score = 0

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gained = reveal_cross(
                    self.tilemap,
                    self.player.gx,
                    self.player.gy,
                    treasure_score=self.cfg.treasure_score,
                )
                self.score += gained

    def handle_input(self, now_ms: int) -> None:
        keys = pygame.key.get_pressed()
        if now_ms - self.player.last_step_ms < self.cfg.player_step_cooldown_ms:
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

    def update(self, now_ms: int) -> None:
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

        now_ms = pygame.time.get_ticks()
        for m in self.mummies:
            m.update(
                tilemap=self.tilemap,
                player_gx=self.player.gx,
                player_gy=self.player.gy,
                now_ms=now_ms,
            )

        # Colisión: si alguna momia está en la casilla del jugador
        mummy_positions = [(m.gx, m.gy) for m in self.mummies]
        if any_entity_on_player((self.player.gx, self.player.gy), mummy_positions):
            self.player.take_hit(now_ms)


    def draw(self) -> None:
        self.renderer.draw_world(
            tilemap=self.tilemap,
            player=self.player,
            camera=self.camera,
            score=self.score,
            mummies=self.mummies,
        )
        pygame.display.flip()
